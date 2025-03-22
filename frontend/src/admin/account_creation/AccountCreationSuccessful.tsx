
import React from "react";

interface AccountCreationSuccessfulProps {
    dismissFunction: () => void,
    accountType: string
}

export default class AccountCreationSuccessful extends React.Component<AccountCreationSuccessfulProps> {
    render() {
        return <div data-testid="account-creation-success" className="success-container">
            Account Created Successfully! <br/>
            <button className="btn btn-primary" onClick={() => this.props.dismissFunction()}>Create another {this.props.accountType}</button>
        </div>;
    }
}