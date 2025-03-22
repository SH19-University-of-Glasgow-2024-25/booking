import React, { useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import AccountCreationSuccessful from "./AccountCreationSuccessful";

function CreateCustomer() {
    
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [lastName, setLastName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [organisation, setOrganisation] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [altPhoneNumber, setAltPhoneNumber] = useState('');
    const [notes, setNotes] = useState('');
    const [address, setAddress] = useState('');
    const [postcode, setPostcode] = useState('');

    const [formStyle, setFormStyle] = useState({});

    const [errorElm, setErrorElm] = useState<JSX.Element | null>(null);
    const [successElm, setSuccessElm] = useState<JSX.Element | null>(null);

    const clearForm = () => {
        setEmail("");
        setPassword("");
        setConfirmPassword("");
        setFirstName("");
        setLastName("");
        setPhoneNumber("");
        setAltPhoneNumber("");
        setNotes("");
        setAddress("");
        setPostcode("");
    }
    
    const submitRegistration = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();
        console.log("submitting customer reg form");
        const returnData = {
            email: email,
            password: password,
            confirm_password: confirmPassword,
            first_name: firstName,
            last_name: lastName,
            organisation: organisation,
            phone_number: phoneNumber,
            alt_phone_number: altPhoneNumber,
            notes: notes,
            address: address,
            postcode: postcode,
            type: "customer",
        }
        apiClient.post("/register-admin/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Registration Successful:", res.data);
                    setSuccessElm(<AccountCreationSuccessful dismissFunction={() => {
                        setFormStyle({});
                        setSuccessElm(<></>);
                    }} accountType="Customer"/>);
                    clearForm();
                    setFormStyle({display: "none"});
                    setErrorElm(<></>);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    }

    return (
        <>
        {successElm}
        <form onSubmit={submitRegistration} style={formStyle}>
            <h3>Create Customer</h3>
            <div className="mb-1">
                <label className="form-label">First Name *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-customer-first-name-input"
                    value={firstName}
                    onChange={(e) => setFirstName(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Last Name *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-customer-last-name-input"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Organisation *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-customer-organisation-input"
                    value={organisation}
                    onChange={(e) => setOrganisation(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Email *</label>
                <input
                    className="form-control"
                    type="email"
                    data-testid="create-customer-email-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Address *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-customer-address-input"
                    value={address}
                    onChange={(e) => setAddress(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Postcode *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-customer-postcode-input"
                    value={postcode}
                    onChange={(e) => setPostcode(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Phone Number</label>
                <input
                    className="form-control"
                    type="tel"
                    data-testid="create-customer-phone-number-input"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Alt Phone Number</label>
                <input
                    className="form-control"
                    type="tel"
                    data-testid="create-customer-alternative-phone-number-input"
                    value={altPhoneNumber}
                    onChange={(e) => setAltPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Notes</label>
                <textarea
                    className="form-control"
                    data-testid="create-customer-notes-input"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Password *</label>
                <input
                    className="form-control"
                    type="password"
                    data-testid="create-customer-password-input"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Confirm Password *</label>
                <input
                    className="form-control"
                    type="password"
                    data-testid="create-customer-confirm-password-input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />
            </div>
            {errorElm}
            <button className="btn btn-primary" data-testid="create-customer-submit-button" type="submit">Register Customer</button>
        </form>
        </>
    )
}

export default CreateCustomer;