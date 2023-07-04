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
