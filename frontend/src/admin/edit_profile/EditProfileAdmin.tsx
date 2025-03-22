import { useEffect, useState } from 'react';
import EditProfile from '../../profile/EditProfile';
import apiClient from '../../utilities/apiClient';
import { GenerateErrorDisplayElement } from '../../utilities/Error';

export default function EditProfileAdminPage() {
    const [account, setAccount] = useState<string>("");
    const [admins, setAdmins] = useState<string[]>([]);
    const [interpreters, setInterpreters] = useState<string[]>([]);
    const [customers, setCustomers] = useState<string[]>([]);
    const [errorElm, setErrorElm] = useState(<></>);

    useEffect(() => {
        apiClient.get("/emails/")
            .then((res) => {
                if (res.data.status == "success") {
                    // to see this page there must be at least one admin
                    setAccount(res.data.result.admins[0]);

                    setAdmins(res.data.result.admins);
                    setCustomers(res.data.result.customers);
                    setInterpreters(res.data.result.interpreters);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    }, []);
    
    return (
        <>
        <div className="main-container container d-md-flex justify-content-between">
            <div className="col-lg-7 col-md-8">
                <h3>Edit user</h3>
                {errorElm}
                <div className="mb-4">
                    <label htmlFor="account" style={{"marginBottom": "10px"}}>
                        Choose an Account:
                    </label>
                    <select className="form-select" id="account" data-testid="account-select" value={account} onChange={(e) => setAccount(e.target.value)}>
                        <optgroup label="Admin">
                        {admins.map((admin) => (
                            <option key={admin} value={admin}>
                            {admin}
                            </option>
                        ))}
                        </optgroup>
                        <optgroup label="Customers">
                        {customers.map((customer) => (
                            <option key={customer} value={customer}>
                            {customer}
                            </option>
                        ))}
                        </optgroup>
                        <optgroup label="Interpreters">
                        {interpreters.map((interpreter) => (
                            <option key={interpreter} value={interpreter}>
                            {interpreter}
                            </option>
                        ))}
                        </optgroup>
                    </select>
                </div>
                <div className="border-top pt-3">
                    {
                        admins.length +
                        customers.length +
                        interpreters.length != 0 &&
                        <EditProfile user={account}/>
                    }
                </div>
            </div>

            <div className="col-md-3">
                <div className="px-3 pt-2 ms-4 border-start border-danger bg-body-tertiary mt-3 pb-2">
                    <h5>
                        <i className="bi bi-exclamation-triangle-fill me-2 text-danger"></i>
                        Make sure that...
                    </h5>
                    
                    Any information that is entered is accurate, relevant, 
                    and limited to what is necessary, <a href="https://ico.org.uk/for-organisations/uk-gdpr-guidance-and-resources/data-protection-principles/a-guide-to-the-data-protection-principles/" className="link-secondary">as required under Data Protection law</a>.
                </div>
                <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                    <b>Notes</b> can be used to record details about a user, accessible only to admins.
                </div>
            </div>
        </div>
        </>
    );
}