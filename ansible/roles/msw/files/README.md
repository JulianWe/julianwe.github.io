# MultiSigEthereumWallet - Smart Contract tutorial 🐇

![](../images/soliditywallet.jpg)

**This Tutorial shows how to write, deploy and interact with your own ethereum multisig wallet**


**1. Download and install MetaMask wallet**

[Download Wallet](https://metamask.io/)

**2. Request Rinkeby testnetwork tokens for transaction fee**

[Rinkeby Faucet](https://faucet.rinkeby.io/)

**3. open Remix - Ethereum Web IDE:**

[Remix Ethereum IDE](https://remix.ethereum.org/)


**4. Create Solidity Smart Contract file MultiSigWallet.sol in Remix IDE**

```java
pragma solidity ^0.4.0;
pragma experimental ABIEncoderV2;

contract MultiSigWallet {

    uint minApprovers;
    address beneficiary;
    address owner;
    mapping (address => bool) approvedBy;
    mapping (address => bool) isApprover;
    uint approvalsNum;

    constructor (

        // List of approvers and minimum number of approvers 
        address[] _approvers,
        // 
        uint _minApprovers,
        // beneficiary address will receive all the funds after minimum number of approvals
        address _beneficiary

    ) public payable {

        // check if approvers are more than minApprovers to allow withdraw 
        require(_minApprovers <= _approvers.length, "Required number of approvers should be less than number of approvers");

        minApprovers = _minApprovers;
        beneficiary = _beneficiary;
        owner = msg.sender;

        // store and populate isApprover address mapping 
        for (uint i = 0; i < _approvers.length; i++){

            address approver = _approvers[i];
            isApprover[approver] = true;
        }
    }

    // function to approve spendig funds from contract
    function approve() public {

        // check if callers has rigths to approve this transaction
        require(isApprover[msg.sender], "Not an approver");

        // if caller has not yet approved 
        if(!approvedBy[msg.sender]){

            // increase number of approvals
            approvalsNum++;
            // to ensure that the same approver does not approve a transaction twice  set aproved by to true
            approvedBy[msg.sender] = true;
        }

        // check if we have enough approvals to send funds from contract to beneficiary address
        if (approvalsNum == minApprovers){
            
            // send contract balance to beneficiary address 
            beneficiary.send(address(this).balance);
            // dedestroy contract and return funds to owner if send fails because of wrong address
            selfdestruct(owner);
        }
        
    }

    // function to reject spending if sender is not one of the Multi Sig Wallet approver. In this case send funds to owner.
    function reject() public {

        // check if callers has rigths to approve this transaction
        require(isApprover[msg.sender], "Not an approver");
        // destroy smart contract if caller is approver 
        selfdestruct(owner);
    }


}
```

**5. deploy MultiSigWallet.sol solidity contract with `_APPROVERS`, address[] set to: `["0xB345BD9ff34DeFf59526DF03B0A41d5E7C54bC72","0xd32bac5c062e89912d067f7221e94fe77343D35a","0x0f0d2bf29aae4e6d8d646f967df8c49b28df05e5"]`, and `_MINAPPROVERS` for example to uint `1` (minimum required approvals to execute approve function and send funds to `_BENEFICIARY` address `0xB345BD9ff34DeFf59526DF03B0A41d5E7C54bC72`.**


![](../images/DeployMultiSigWallet.png)



**Approve Spending Wallet funds with one of the approver `_APPROVERS` address**
![](../images/ApproveSpendingWalletFunds.jpg)



**Example contract creation transaction on testnet blockchain explorer**
[Contract creation Etherscan Link](https://ropsten.etherscan.io/tx/0x85e6e933d6fef3ffda240ee6b757e52c42fbb49a1dd74caa7df8d3bcc5002009)
[Contract approval Etherscan Link](https://ropsten.etherscan.io/tx/0x9995326e362c6d18be4559c7b0e36525c96608ea1228d33f74003ff95a5b6e7e)
