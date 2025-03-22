import React, { useState } from "react";
import apiClient from "../../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import AccountCreationSuccessful from "./AccountCreationSuccessful";

function CreateAdmin() {

    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [lastName, setLastName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [altPhoneNumber, setAltPhoneNumber] = useState('');
    const [notes, setNotes] = useState('');

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
            phone_number: phoneNumber,
            alt_phone_number: altPhoneNumber,
            notes: notes,
            type: "admin",
        }
        apiClient.post("/register-admin/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Registration Successful:", res.data);
                    setSuccessElm(<AccountCreationSuccessful dismissFunction={() => {
                        setFormStyle({});
                        setSuccessElm(<></>);
                    }} accountType="Admin"/>);
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
            <h3>Create Admin</h3>
            
            <div className="mb-1">
                <label className="form-label">First Name *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-admin-first-name-input"
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
                    data-testid="create-admin-last-name-input"
                    value={lastName}
                    onChange={(e) => setLastName(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Email *</label>
                <input
                    className="form-control"
                    type="email"
                    data-testid="create-admin-email-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Phone Number</label>
                <input
                    className="form-control"
                    type="tel"
                    data-testid="create-admin-phone-number-input"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Alt Phone Number</label>
                <input
                    className="form-control"
                    type="tel"
                    data-testid="create-admin-alternative-phone-number-input"
                    value={altPhoneNumber}
                    onChange={(e) => setAltPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Notes</label>
                <textarea
                    className="form-control"
                    data-testid="create-admin-notes-input"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Password *</label>
                <input
                    className="form-control"
                    type="password"
                    data-testid="create-admin-password-input"
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
                    data-testid="create-admin-confirm-password-input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />
            </div>
            {errorElm}
            <button className="btn btn-primary" data-testid="create-admin-submit-button" type="submit">Register Admin</button>
        </form>
        </>
    )
}

export default CreateAdmin;