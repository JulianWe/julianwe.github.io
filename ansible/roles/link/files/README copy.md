# How to create a Chainlink Operator Node

![](../chainlink/images/chainlink.jpg)

[Docs](https://docs.chain.link/)


**Run Ethereum Client**
```sh
docker pull ethereum/client-go:latest

mkdir ~/.geth-goerli && cd ~/.geth-goerli

docker run --name eth -p 8546:8546 -v ~/.geth-goerli:/geth -it \
    ethereum/client-go --goerli --ws --ipcdisable \
    --ws.addr 0.0.0.0 --ws.origins="*" --datadir /geth

```


**create alchemy or infura account**
ETH_URL=wss://eth-goerli.alchemyapi.io/v2/YOUR_PROJECT_ID
ETH_URL=wss://goerli.infura.io/ws/v3/YOUR_PROJECT_ID

ETH_URL=wss://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3
https://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3


**create postgres database**
```sh
docker run --name cl-postgres -e POSTGRES_PASSWORD=test0815test0815 -p 5432:5432 -d postgres
```


**create toml config**


```bash
mkdir ~/.chainlink-goerli && cd ~/.chainlink-goerli


echo "[Log]
Level = 'warn'

[WebServer]
AllowOrigins = '*'
SecureCookies = false

[WebServer.TLS]
HTTPSPort = 0

[[EVM]]
ChainID = '5'

[[EVM.Nodes]]
Name = 'Goerli'
WSURL = 'wss://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3'
HTTPURL = 'https://goerli.infura.io/v3/7611c5df22314fbe80f592e4ccce82b3'
" > ~/.chainlink-goerli/config.toml
```


**create database password config**
```sh
echo "[Password]
Keystore = 'test0815test0815'
[Database]
URL = 'postgresql://postgres:test0815test0815@host.docker.internal:5432/postgres?sslmode=disable'
" > ~/.chainlink-goerli/secrets.toml
```


**run chainlink operator container**
```sh
cd ~/.chainlink-goerli && docker run --platform linux/x86_64/v8 --name chainlink -v ~/.chainlink-goerli:/chainlink -it -p 6688:6688 --add-host=host.docker.internal:host-gateway smartcontract/chainlink:2.0.0 node -config /chainlink/config.toml -secrets /chainlink/secrets.toml start

Enter API EMail:
Enter API Password:
```

**Connect chainlink UI**
http://localhost:6688

![](../chainlink/images/Operator.jpg)








# How to setup your own Operator Smart Contract

[Chainlink Testnet Token](https://faucets.chain.link/goerli)
[Chainlink Docs Fulfilling Request](https://docs.chain.link/chainlink-nodes/v1/fulfilling-requests)


[Remix Ethereum IDE](https://remix.ethereum.org/#url=https://docs.chain.link/samples/ChainlinkNodes/Operator.sol&lang=en&optimize=false&runs=200&evmVersion=null&version=soljson-v0.7.6+commit.7338295f.js)

**In Remix IDE Select compiler version '0.7.6'**
```java
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;
import "@chainlink/contracts/src/v0.7/Operator.sol";

or
// SPDX-License-Identifier: MIT
pragma solidity ^0.7.6;

import "./AuthorizedReceiver.sol";
import "./LinkTokenReceiver.sol";
import "./ConfirmedOwner.sol";
import "./interfaces/LinkTokenInterface.sol";
import "./interfaces/OperatorInterface.sol";
import "./interfaces/OwnableInterface.sol";
import "./interfaces/WithdrawalInterface.sol";
import "./vendor/Address.sol";
import "./vendor/SafeMathChainlink.sol";

/**
 * @title The Chainlink Operator contract
 * @notice Node operators can deploy this contract to fulfill requests sent to them
 */
contract Operator is AuthorizedReceiver, ConfirmedOwner, LinkTokenReceiver, OperatorInterface, WithdrawalInterface {
  using Address for address;
  using SafeMathChainlink for uint256;

  struct Commitment {
    bytes31 paramsHash;
    uint8 dataVersion;
  }

  uint256 public constant getExpiryTime = 5 minutes;
  uint256 private constant MAXIMUM_DATA_VERSION = 256;
  uint256 private constant MINIMUM_CONSUMER_GAS_LIMIT = 400000;
  uint256 private constant SELECTOR_LENGTH = 4;
  uint256 private constant EXPECTED_REQUEST_WORDS = 2;
  uint256 private constant MINIMUM_REQUEST_LENGTH = SELECTOR_LENGTH + (32 * EXPECTED_REQUEST_WORDS);
  // We initialize fields to 1 instead of 0 so that the first invocation
  // does not cost more gas.
  uint256 private constant ONE_FOR_CONSISTENT_GAS_COST = 1;
  // oracleRequest is intended for version 1, enabling single word responses
  bytes4 private constant ORACLE_REQUEST_SELECTOR = this.oracleRequest.selector;
  // operatorRequest is intended for version 2, enabling multi-word responses
  bytes4 private constant OPERATOR_REQUEST_SELECTOR = this.operatorRequest.selector;

  LinkTokenInterface internal immutable linkToken;
  mapping(bytes32 => Commitment) private s_commitments;
  mapping(address => bool) private s_owned;
  // Tokens sent for requests that have not been fulfilled yet
  uint256 private s_tokensInEscrow = ONE_FOR_CONSISTENT_GAS_COST;

  event OracleRequest(
    bytes32 indexed specId,
    address requester,
    bytes32 requestId,
    uint256 payment,
    address callbackAddr,
    bytes4 callbackFunctionId,
    uint256 cancelExpiration,
    uint256 dataVersion,
    bytes data
  );

  event CancelOracleRequest(bytes32 indexed requestId);

  event OracleResponse(bytes32 indexed requestId);

  event OwnableContractAccepted(address indexed acceptedContract);

  event TargetsUpdatedAuthorizedSenders(address[] targets, address[] senders, address changedBy);

  /**
   * @notice Deploy with the address of the LINK token
   * @dev Sets the LinkToken address for the imported LinkTokenInterface
   * @param link The address of the LINK token
   * @param owner The address of the owner
   */
  constructor(address link, address owner) ConfirmedOwner(owner) {
    linkToken = LinkTokenInterface(link); // external but already deployed and unalterable
  }

  /**
   * @notice The type and version of this contract
   * @return Type and version string
   */
  function typeAndVersion() external pure virtual returns (string memory) {
    return "Operator 1.0.0";
  }

  /**
   * @notice Creates the Chainlink request. This is a backwards compatible API
   * with the Oracle.sol contract, but the behavior changes because
   * callbackAddress is assumed to be the same as the request sender.
   * @param callbackAddress The consumer of the request
   * @param payment The amount of payment given (specified in wei)
   * @param specId The Job Specification ID
   * @param callbackAddress The address the oracle data will be sent to
   * @param callbackFunctionId The callback function ID for the response
   * @param nonce The nonce sent by the requester
   * @param dataVersion The specified data version
   * @param data The extra request parameters
   */
  function oracleRequest(
    address sender,
    uint256 payment,
    bytes32 specId,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 nonce,
    uint256 dataVersion,
    bytes calldata data
  ) external override validateFromLINK {
    (bytes32 requestId, uint256 expiration) = _verifyAndProcessOracleRequest(
      sender,
      payment,
      callbackAddress,
      callbackFunctionId,
      nonce,
      dataVersion
    );
    emit OracleRequest(specId, sender, requestId, payment, sender, callbackFunctionId, expiration, dataVersion, data);
  }

  /**
   * @notice Creates the Chainlink request
   * @dev Stores the hash of the params as the on-chain commitment for the request.
   * Emits OracleRequest event for the Chainlink node to detect.
   * @param sender The sender of the request
   * @param payment The amount of payment given (specified in wei)
   * @param specId The Job Specification ID
   * @param callbackFunctionId The callback function ID for the response
   * @param nonce The nonce sent by the requester
   * @param dataVersion The specified data version
   * @param data The extra request parameters
   */
  function operatorRequest(
    address sender,
    uint256 payment,
    bytes32 specId,
    bytes4 callbackFunctionId,
    uint256 nonce,
    uint256 dataVersion,
    bytes calldata data
  ) external override validateFromLINK {
    (bytes32 requestId, uint256 expiration) = _verifyAndProcessOracleRequest(
      sender,
      payment,
      sender,
      callbackFunctionId,
      nonce,
      dataVersion
    );
    emit OracleRequest(specId, sender, requestId, payment, sender, callbackFunctionId, expiration, dataVersion, data);
  }

  /**
   * @notice Called by the Chainlink node to fulfill requests
   * @dev Given params must hash back to the commitment stored from `oracleRequest`.
   * Will call the callback address' callback function without bubbling up error
   * checking in a `require` so that the node can get paid.
   * @param requestId The fulfillment request ID that must match the requester's
   * @param payment The payment amount that will be released for the oracle (specified in wei)
   * @param callbackAddress The callback address to call for fulfillment
   * @param callbackFunctionId The callback function ID to use for fulfillment
   * @param expiration The expiration that the node should respond by before the requester can cancel
   * @param data The data to return to the consuming contract
   * @return Status if the external call was successful
   */
  function fulfillOracleRequest(
    bytes32 requestId,
    uint256 payment,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 expiration,
    bytes32 data
  )
    external
    override
    validateAuthorizedSender
    validateRequestId(requestId)
    validateCallbackAddress(callbackAddress)
    returns (bool)
  {
    _verifyOracleRequestAndProcessPayment(requestId, payment, callbackAddress, callbackFunctionId, expiration, 1);
    emit OracleResponse(requestId);
    require(gasleft() >= MINIMUM_CONSUMER_GAS_LIMIT, "Must provide consumer enough gas");
    // All updates to the oracle's fulfillment should come before calling the
    // callback(addr+functionId) as it is untrusted.
    // See: https://solidity.readthedocs.io/en/develop/security-considerations.html#use-the-checks-effects-interactions-pattern
    (bool success, ) = callbackAddress.call(abi.encodeWithSelector(callbackFunctionId, requestId, data)); // solhint-disable-line avoid-low-level-calls
    return success;
  }

  /**
   * @notice Called by the Chainlink node to fulfill requests with multi-word support
   * @dev Given params must hash back to the commitment stored from `oracleRequest`.
   * Will call the callback address' callback function without bubbling up error
   * checking in a `require` so that the node can get paid.
   * @param requestId The fulfillment request ID that must match the requester's
   * @param payment The payment amount that will be released for the oracle (specified in wei)
   * @param callbackAddress The callback address to call for fulfillment
   * @param callbackFunctionId The callback function ID to use for fulfillment
   * @param expiration The expiration that the node should respond by before the requester can cancel
   * @param data The data to return to the consuming contract
   * @return Status if the external call was successful
   */
  function fulfillOracleRequest2(
    bytes32 requestId,
    uint256 payment,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 expiration,
    bytes calldata data
  )
    external
    override
    validateAuthorizedSender
    validateRequestId(requestId)
    validateCallbackAddress(callbackAddress)
    validateMultiWordResponseId(requestId, data)
    returns (bool)
  {
    _verifyOracleRequestAndProcessPayment(requestId, payment, callbackAddress, callbackFunctionId, expiration, 2);
    emit OracleResponse(requestId);
    require(gasleft() >= MINIMUM_CONSUMER_GAS_LIMIT, "Must provide consumer enough gas");
    // All updates to the oracle's fulfillment should come before calling the
    // callback(addr+functionId) as it is untrusted.
    // See: https://solidity.readthedocs.io/en/develop/security-considerations.html#use-the-checks-effects-interactions-pattern
    (bool success, ) = callbackAddress.call(abi.encodePacked(callbackFunctionId, data)); // solhint-disable-line avoid-low-level-calls
    return success;
  }

  /**
   * @notice Transfer the ownership of ownable contracts. This is primarily
   * intended for Authorized Forwarders but could possibly be extended to work
   * with future contracts.
   * @param ownable list of addresses to transfer
   * @param newOwner address to transfer ownership to
   */
  function transferOwnableContracts(address[] calldata ownable, address newOwner) external onlyOwner {
    for (uint256 i = 0; i < ownable.length; i++) {
      s_owned[ownable[i]] = false;
      OwnableInterface(ownable[i]).transferOwnership(newOwner);
    }
  }

  /**
   * @notice Accept the ownership of an ownable contract. This is primarily
   * intended for Authorized Forwarders but could possibly be extended to work
   * with future contracts.
   * @dev Must be the pending owner on the contract
   * @param ownable list of addresses of Ownable contracts to accept
   */
  function acceptOwnableContracts(address[] calldata ownable) public validateAuthorizedSenderSetter {
    for (uint256 i = 0; i < ownable.length; i++) {
      s_owned[ownable[i]] = true;
      emit OwnableContractAccepted(ownable[i]);
      OwnableInterface(ownable[i]).acceptOwnership();
    }
  }

  /**
   * @notice Sets the fulfillment permission for
   * @param targets The addresses to set permissions on
   * @param senders The addresses that are allowed to send updates
   */
  function setAuthorizedSendersOn(address[] calldata targets, address[] calldata senders)
    public
    validateAuthorizedSenderSetter
  {
    TargetsUpdatedAuthorizedSenders(targets, senders, msg.sender);

    for (uint256 i = 0; i < targets.length; i++) {
      AuthorizedReceiverInterface(targets[i]).setAuthorizedSenders(senders);
    }
  }

  /**
   * @notice Accepts ownership of ownable contracts and then immediately sets
   * the authorized sender list on each of the newly owned contracts. This is
   * primarily intended for Authorized Forwarders but could possibly be
   * extended to work with future contracts.
   * @param targets The addresses to set permissions on
   * @param senders The addresses that are allowed to send updates
   */
  function acceptAuthorizedReceivers(address[] calldata targets, address[] calldata senders)
    external
    validateAuthorizedSenderSetter
  {
    acceptOwnableContracts(targets);
    setAuthorizedSendersOn(targets, senders);
  }

  /**
   * @notice Allows the node operator to withdraw earned LINK to a given address
   * @dev The owner of the contract can be another wallet and does not have to be a Chainlink node
   * @param recipient The address to send the LINK token to
   * @param amount The amount to send (specified in wei)
   */
  function withdraw(address recipient, uint256 amount)
    external
    override(OracleInterface, WithdrawalInterface)
    onlyOwner
    validateAvailableFunds(amount)
  {
    assert(linkToken.transfer(recipient, amount));
  }

  /**
   * @notice Displays the amount of LINK that is available for the node operator to withdraw
   * @dev We use `ONE_FOR_CONSISTENT_GAS_COST` in place of 0 in storage
   * @return The amount of withdrawable LINK on the contract
   */
  function withdrawable() external view override(OracleInterface, WithdrawalInterface) returns (uint256) {
    return _fundsAvailable();
  }

  /**
   * @notice Forward a call to another contract
   * @dev Only callable by the owner
   * @param to address
   * @param data to forward
   */
  function ownerForward(address to, bytes calldata data) external onlyOwner validateNotToLINK(to) {
    require(to.isContract(), "Must forward to a contract");
    (bool status, ) = to.call(data);
    require(status, "Forwarded call failed");
  }

  /**
   * @notice Interact with other LinkTokenReceiver contracts by calling transferAndCall
   * @param to The address to transfer to.
   * @param value The amount to be transferred.
   * @param data The extra data to be passed to the receiving contract.
   * @return success bool
   */
  function ownerTransferAndCall(
    address to,
    uint256 value,
    bytes calldata data
  ) external override onlyOwner validateAvailableFunds(value) returns (bool success) {
    return linkToken.transferAndCall(to, value, data);
  }

  /**
   * @notice Distribute funds to multiple addresses using ETH send
   * to this payable function.
   * @dev Array length must be equal, ETH sent must equal the sum of amounts.
   * A malicious receiver could cause the distribution to revert, in which case
   * it is expected that the address is removed from the list.
   * @param receivers list of addresses
   * @param amounts list of amounts
   */
  function distributeFunds(address payable[] calldata receivers, uint256[] calldata amounts) external payable {
    require(receivers.length > 0 && receivers.length == amounts.length, "Invalid array length(s)");
    uint256 valueRemaining = msg.value;
    for (uint256 i = 0; i < receivers.length; i++) {
      uint256 sendAmount = amounts[i];
      valueRemaining = valueRemaining.sub(sendAmount);
      receivers[i].transfer(sendAmount);
    }
    require(valueRemaining == 0, "Too much ETH sent");
  }

  /**
   * @notice Allows recipient to cancel requests sent to this oracle contract.
   * Will transfer the LINK sent for the request back to the recipient address.
   * @dev Given params must hash to a commitment stored on the contract in order
   * for the request to be valid. Emits CancelOracleRequest event.
   * @param requestId The request ID
   * @param payment The amount of payment given (specified in wei)
   * @param callbackFunc The requester's specified callback function selector
   * @param expiration The time of the expiration for the request
   */
  function cancelOracleRequest(
    bytes32 requestId,
    uint256 payment,
    bytes4 callbackFunc,
    uint256 expiration
  ) external override {
    bytes31 paramsHash = _buildParamsHash(payment, msg.sender, callbackFunc, expiration);
    require(s_commitments[requestId].paramsHash == paramsHash, "Params do not match request ID");
    // solhint-disable-next-line not-rely-on-time
    require(expiration <= block.timestamp, "Request is not expired");

    delete s_commitments[requestId];
    emit CancelOracleRequest(requestId);

    linkToken.transfer(msg.sender, payment);
  }

  /**
   * @notice Allows requester to cancel requests sent to this oracle contract.
   * Will transfer the LINK sent for the request back to the recipient address.
   * @dev Given params must hash to a commitment stored on the contract in order
   * for the request to be valid. Emits CancelOracleRequest event.
   * @param nonce The nonce used to generate the request ID
   * @param payment The amount of payment given (specified in wei)
   * @param callbackFunc The requester's specified callback function selector
   * @param expiration The time of the expiration for the request
   */
  function cancelOracleRequestByRequester(
    uint256 nonce,
    uint256 payment,
    bytes4 callbackFunc,
    uint256 expiration
  ) external {
    bytes32 requestId = keccak256(abi.encodePacked(msg.sender, nonce));
    bytes31 paramsHash = _buildParamsHash(payment, msg.sender, callbackFunc, expiration);
    require(s_commitments[requestId].paramsHash == paramsHash, "Params do not match request ID");
    // solhint-disable-next-line not-rely-on-time
    require(expiration <= block.timestamp, "Request is not expired");

    delete s_commitments[requestId];
    emit CancelOracleRequest(requestId);

    linkToken.transfer(msg.sender, payment);
  }

  /**
   * @notice Returns the address of the LINK token
   * @dev This is the public implementation for chainlinkTokenAddress, which is
   * an internal method of the ChainlinkClient contract
   */
  function getChainlinkToken() public view override returns (address) {
    return address(linkToken);
  }

  /**
   * @notice Require that the token transfer action is valid
   * @dev OPERATOR_REQUEST_SELECTOR = multiword, ORACLE_REQUEST_SELECTOR = singleword
   */
  function _validateTokenTransferAction(bytes4 funcSelector, bytes memory data) internal pure override {
    require(data.length >= MINIMUM_REQUEST_LENGTH, "Invalid request length");
    require(
      funcSelector == OPERATOR_REQUEST_SELECTOR || funcSelector == ORACLE_REQUEST_SELECTOR,
      "Must use whitelisted functions"
    );
  }

  /**
   * @notice Verify the Oracle Request and record necessary information
   * @param sender The sender of the request
   * @param payment The amount of payment given (specified in wei)
   * @param callbackAddress The callback address for the response
   * @param callbackFunctionId The callback function ID for the response
   * @param nonce The nonce sent by the requester
   */
  function _verifyAndProcessOracleRequest(
    address sender,
    uint256 payment,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 nonce,
    uint256 dataVersion
  ) private validateNotToLINK(callbackAddress) returns (bytes32 requestId, uint256 expiration) {
    requestId = keccak256(abi.encodePacked(sender, nonce));
    require(s_commitments[requestId].paramsHash == 0, "Must use a unique ID");
    // solhint-disable-next-line not-rely-on-time
    expiration = block.timestamp.add(getExpiryTime);
    bytes31 paramsHash = _buildParamsHash(payment, callbackAddress, callbackFunctionId, expiration);
    s_commitments[requestId] = Commitment(paramsHash, _safeCastToUint8(dataVersion));
    s_tokensInEscrow = s_tokensInEscrow.add(payment);
    return (requestId, expiration);
  }

  /**
   * @notice Verify the Oracle request and unlock escrowed payment
   * @param requestId The fulfillment request ID that must match the requester's
   * @param payment The payment amount that will be released for the oracle (specified in wei)
   * @param callbackAddress The callback address to call for fulfillment
   * @param callbackFunctionId The callback function ID to use for fulfillment
   * @param expiration The expiration that the node should respond by before the requester can cancel
   */
  function _verifyOracleRequestAndProcessPayment(
    bytes32 requestId,
    uint256 payment,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 expiration,
    uint256 dataVersion
  ) internal {
    bytes31 paramsHash = _buildParamsHash(payment, callbackAddress, callbackFunctionId, expiration);
    require(s_commitments[requestId].paramsHash == paramsHash, "Params do not match request ID");
    require(s_commitments[requestId].dataVersion <= _safeCastToUint8(dataVersion), "Data versions must match");
    s_tokensInEscrow = s_tokensInEscrow.sub(payment);
    delete s_commitments[requestId];
  }

  /**
   * @notice Build the bytes31 hash from the payment, callback and expiration.
   * @param payment The payment amount that will be released for the oracle (specified in wei)
   * @param callbackAddress The callback address to call for fulfillment
   * @param callbackFunctionId The callback function ID to use for fulfillment
   * @param expiration The expiration that the node should respond by before the requester can cancel
   * @return hash bytes31
   */
  function _buildParamsHash(
    uint256 payment,
    address callbackAddress,
    bytes4 callbackFunctionId,
    uint256 expiration
  ) internal pure returns (bytes31) {
    return bytes31(keccak256(abi.encodePacked(payment, callbackAddress, callbackFunctionId, expiration)));
  }

  /**
   * @notice Safely cast uint256 to uint8
   * @param number uint256
   * @return uint8 number
   */
  function _safeCastToUint8(uint256 number) internal pure returns (uint8) {
    require(number < MAXIMUM_DATA_VERSION, "number too big to cast");
    return uint8(number);
  }

  /**
   * @notice Returns the LINK available in this contract, not locked in escrow
   * @return uint256 LINK tokens available
   */
  function _fundsAvailable() private view returns (uint256) {
    uint256 inEscrow = s_tokensInEscrow.sub(ONE_FOR_CONSISTENT_GAS_COST);
    return linkToken.balanceOf(address(this)).sub(inEscrow);
  }

  /**
   * @notice concrete implementation of AuthorizedReceiver
   * @return bool of whether sender is authorized
   */
  function _canSetAuthorizedSenders() internal view override returns (bool) {
    return isAuthorizedSender(msg.sender) || owner() == msg.sender;
  }

  // MODIFIERS

  /**
   * @dev Reverts if the first 32 bytes of the bytes array is not equal to requestId
   * @param requestId bytes32
   * @param data bytes
   */
  modifier validateMultiWordResponseId(bytes32 requestId, bytes calldata data) {
    require(data.length >= 32, "Response must be > 32 bytes");
    bytes32 firstDataWord;
    assembly {
      firstDataWord := calldataload(data.offset)
    }
    require(requestId == firstDataWord, "First word must be requestId");
    _;
  }

  /**
   * @dev Reverts if amount requested is greater than withdrawable balance
   * @param amount The given amount to compare to `s_withdrawableTokens`
   */
  modifier validateAvailableFunds(uint256 amount) {
    require(_fundsAvailable() >= amount, "Amount requested is greater than withdrawable balance");
    _;
  }

  /**
   * @dev Reverts if request ID does not exist
   * @param requestId The given request ID to check in stored `commitments`
   */
  modifier validateRequestId(bytes32 requestId) {
    require(s_commitments[requestId].paramsHash != 0, "Must have a valid requestId");
    _;
  }

  /**
   * @dev Reverts if the callback address is the LINK token
   * @param to The callback address
   */
  modifier validateNotToLINK(address to) {
    require(to != address(linkToken), "Cannot call to LINK");
    _;
  }

  /**
   * @dev Reverts if the target address is owned by the operator
   */
  modifier validateCallbackAddress(address callbackAddress) {
    require(!s_owned[callbackAddress], "Cannot call owned contract");
    _;
  }
}

```



**[ChainLink Contract Addresses:](https://docs.chain.link/resources/link-token-contracts)** 

**Goerli Testnet: 0x326C977E6efc84E512bB9C30f76E30c160eD06FB**
**Ethereum Mainnet: 0x514910771AF9Ca656af840dff83E8264EcF986CA**
Set 'LINK' 0x326C977E6efc84E512bB9C30f76E30c160eD06FB Goerli Token Testnet contract and 'OWNER' (Wallet Address) values and click transact.
![](../chainlink/images/deploy_contract.jpg)

**Note: the output shows your newly deployed operator smart contract: 0xfc5F20476E6289c7120A89D45e383EB28603152f**
```sh
[view on etherscan](https://goerli.etherscan.io/tx/0xebeea65d9e90c804b049a8d34e115f88ea14ea49b267d2843a2e2ef8f0ee7382)
[block:9412412 txIndex:11]from: 0x0f0...f05E5to: Operator.(constructor)value: 0 weidata: 0x60a...f05e5logs: 0hash: 0xfd1...938e7
status	true Transaction mined and execution succeed
transaction hash	0xebeea65d9e90c804b049a8d34e115f88ea14ea49b267d2843a2e2ef8f0ee7382
block hash	0xfd1c521f5cbd50873b056f5a34176ae2f33137abf326ca15b878c15fdc3938e7
block number	9412412
contract address	0xfc5F20476E6289c7120A89D45e383EB28603152f
from	0x0f0d2BF29AAe4E6D8d646F967Df8c49B28Df05E5
to	Operator.(constructor)
gas	3754948 gas
transaction cost	3754948 gas 
input	0x60a...f05e5
decoded input	{
	"address link": "0x326C977E6efc84E512bB9C30f76E30c160eD06FB",
	"address owner": "0x0f0d2BF29AAe4E6D8d646F967Df8c49B28Df05E5"
}
```


**Copy your Chainlink node address from Operator ui under 'settings' & 'key management': 0x321f40D5D7f678A35DCfC15Df852135F2c53e1AA**
![](../chainlink/images/ChainLink_Operator.jpg)


[Chainlink Smart Contract (v0.7) that we deployed on GitHub](https://github.com/smartcontractkit/chainlink/blob/develop/contracts/src/v0.7/Operator.sol)
With the Following fuctions:
![](../chainlink/images/deployed_contract.jpg)

and call the functions 'setAuthorizedSenders' & 'isAuthorizedSender' with the address of your node (in my case the array: '["0x321f40D5D7f678A35DCfC15Df852135F2c53e1AA"]') to verify that your chainlink node address can call the operator contract. The function must return true. You can use Remix IDE or instead Etherscan: https://goerli.etherscan.io/address/0xfc5f20476e6289c7120a89d45e383eb28603152f#writeContract

![](../chainlink/images/Etherscan_CSC.jpg)


# Add a Job to your Node
To be able to earn Link rewards You will create a job that calls an OpenAPI, parses the response and then return a uint256
In the Chainlink Operator UI on the Jobs tab, click New Job and replace the 'contractAdress' with the newly deployd ChainLink Smart Contract '0x2174C8be4fb7dF9C7c42318643579c3E994CA343'

```sh
type = "directrequest"
schemaVersion = 1
name = "Get > Price"
externalJobID = "6e391cc2-97de-4008-a630-edb1057c3f9c"
forwardingAllowed = false
maxTaskDuration = "0s"
contractAddress = "0x2174C8be4fb7dF9C7c42318643579c3E994CA343"
minContractPaymentLinkJuels = "0"
observationSource = """
    decode_log   [type="ethabidecodelog"
                  abi="OracleRequest(bytes32 indexed specId, address requester, bytes32 requestId, uint256 payment, address callbackAddr, bytes4 callbackFunctionId, uint256 cancelExpiration, uint256 dataVersion, bytes data)"
                  data="$(jobRun.logData)"
                  topics="$(jobRun.logTopics)"]

    decode_cbor  [type="cborparse" data="$(decode_log.data)"]
    fetch        [type="http" method=GET url="$(decode_cbor.get)" allowUnrestrictedNetworkAccess="true"]
    parse        [type="jsonparse" path="$(decode_cbor.path)" data="$(fetch)"]

    multiply     [type="multiply" input="$(parse)" times="$(decode_cbor.times)"]

    encode_data  [type="ethabiencode" abi="(bytes32 requestId, uint256 value)" data="{ \\"requestId\\": $(decode_log.requestId), \\"value\\": $(multiply) }"]
    encode_tx    [type="ethabiencode"
                  abi="fulfillOracleRequest2(bytes32 requestId, uint256 payment, address callbackAddress, bytes4 callbackFunctionId, uint256 expiration, bytes calldata data)"
                  data="{\\"requestId\\": $(decode_log.requestId), \\"payment\\":   $(decode_log.payment), \\"callbackAddress\\": $(decode_log.callbackAddr), \\"callbackFunctionId\\": $(decode_log.callbackFunctionId), \\"expiration\\": $(decode_log.cancelExpiration), \\"data\\": $(encode_data)}"
                  ]
    submit_tx    [type="ethtx" to="0x2174C8be4fb7dF9C7c42318643579c3E994CA343" data="$(encode_tx)"]

    decode_log -> decode_cbor -> fetch -> parse -> multiply -> encode_data -> encode_tx -> submit_tx
"""
```

https://goerli.etherscan.io/address/0x5fa7f2926bd6f490cfcf29245cd3f7bb29a8ceed#writeContract


**Copy your External _jobId: 6e391cc2-97de-4008-a630-edb1057c3f9c without dashes for the consumer contract**


# create testnet consumer contract

https://remix.ethereum.org/#url=https://docs.chain.link/samples/APIRequests/ATestnetConsumer.sol&lang=en&optimize=false&runs=200&evmVersion=null&version=soljson-v0.8.18+commit.87f61d96.js

```java
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "@chainlink/contracts/src/v0.8/ChainlinkClient.sol";
import "@chainlink/contracts/src/v0.8/ConfirmedOwner.sol";

/**
 * THIS IS AN EXAMPLE CONTRACT THAT USES UN-AUDITED CODE.
 * DO NOT USE THIS CODE IN PRODUCTION.
 */

contract ATestnetConsumer is ChainlinkClient, ConfirmedOwner {
    using Chainlink for Chainlink.Request;

    uint256 private constant ORACLE_PAYMENT = (1 * LINK_DIVISIBILITY) / 10; // 0.1 * 10**18
    uint256 public currentPrice;

    event RequestEthereumPriceFulfilled(
        bytes32 indexed requestId,
        uint256 indexed price
    );

    /**
     *  Sepolia
     *@dev LINK address in Goerli network: 0x326C977E6efc84E512bB9C30f76E30c160eD06FB
     * @dev Check https://docs.chain.link/docs/link-token-contracts/ for LINK address for the right network
     */
    constructor() ConfirmedOwner(msg.sender) {
        setChainlinkToken(0x326C977E6efc84E512bB9C30f76E30c160eD06FB);
    }

    function requestEthereumPrice(
        address _oracle,
        string memory _jobId
    ) public onlyOwner {
        Chainlink.Request memory req = buildChainlinkRequest(
            stringToBytes32(_jobId),
            address(this),
            this.fulfillEthereumPrice.selector
        );
        req.add(
            "get",
            "https://min-api.cryptocompare.com/data/price?fsym=ETH&tsyms=USD"
        );
        req.add("path", "USD");
        req.addInt("times", 100);
        sendChainlinkRequestTo(_oracle, req, ORACLE_PAYMENT);
    }

    function fulfillEthereumPrice(
        bytes32 _requestId,
        uint256 _price
    ) public recordChainlinkFulfillment(_requestId) {
        emit RequestEthereumPriceFulfilled(_requestId, _price);
        currentPrice = _price;
    }

    function getChainlinkToken() public view returns (address) {
        return chainlinkTokenAddress();
    }

    function withdrawLink() public onlyOwner {
        LinkTokenInterface link = LinkTokenInterface(chainlinkTokenAddress());
        require(
            link.transfer(msg.sender, link.balanceOf(address(this))),
            "Unable to transfer"
        );
    }

    function cancelRequest(
        bytes32 _requestId,
        uint256 _payment,
        bytes4 _callbackFunctionId,
        uint256 _expiration
    ) public onlyOwner {
        cancelChainlinkRequest(
            _requestId,
            _payment,
            _callbackFunctionId,
            _expiration
        );
    }

    function stringToBytes32(
        string memory source
    ) private pure returns (bytes32 result) {
        bytes memory tempEmptyStringTest = bytes(source);
        if (tempEmptyStringTest.length == 0) {
            return 0x0;
        }

        assembly {
            // solhint-disable-line no-inline-assembly
            result := mload(add(source, 32))
        }
    }
}
```



call the contract function 'requestEthereumPrice' set '_oracle' 0x2174C8be4fb7dF9C7c42318643579c3E994CA343  & '_jobId' '6e391cc297de4008a630edb1057c3f9c' variables
