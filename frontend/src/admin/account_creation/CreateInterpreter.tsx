import React, { useEffect, useState } from "react";
import apiClient from "../../utilities/apiClient";
import Select, {MultiValue} from "react-select";
import {GenerateErrorDisplayElement} from "../../utilities/Error";
import AccountCreationSuccessful from "./AccountCreationSuccessful";

function CreateInterpreter() {
    
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [lastName, setLastName] = useState('');
    const [firstName, setFirstName] = useState('');
    const [phoneNumber, setPhoneNumber] = useState('');
    const [altPhoneNumber, setAltPhoneNumber] = useState('');
    const [notes, setNotes] = useState('');
    const [address, setAddress] = useState('');
    const [postcode, setPostcode] = useState('');
    const [gender, setGender] = useState('');
    const [languages, setLanguages] = useState<MultiValue<{ value: string; label: string }>>([]);
    const [languageOptions, setLanguageOptions] = useState([]);

    const [formStyle, setFormStyle] = useState({});

    const [errorElm, setErrorElm] = useState<JSX.Element | null>(null);
    const [successElm, setSuccessElm] = useState<JSX.Element | null>(null);

    const fetchData = () => {
        apiClient.get("/languages/")
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Language Retrieval Successful:", res.data);
                    const formattedOptions = res.data.result.languages.map((lang:string) => ({
                        value: lang,
                        label: lang,
                    }));
                    setLanguageOptions(formattedOptions);
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };

    useEffect(() => {
        fetchData();
    }, []);

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
        setGender("");
        setLanguages([]);
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
            address: address,
            postcode: postcode,
            gender: gender,
            languages: languages.map((language) => language.value),
            type: "interpreter",
        }
        apiClient.post("/register-admin/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Registration Successful:", res.data);
                    setSuccessElm(<AccountCreationSuccessful dismissFunction={() => {
                        setFormStyle({});
                        setSuccessElm(<></>);
                    }} accountType="Interpreter"/>);
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
            <h3>Create Interpreter</h3>
            <div className="mb-1">
                <label className="form-label">First Name *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-interpreter-first-name-input"
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
                    data-testid="create-interpreter-last-name-input"
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
                    data-testid="create-interpreter-email-input"
                    value={email}
                    onChange={(e) => setEmail(e.target.value)}
                    required
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Languages *</label>
                <div data-testid="create-interpreter-language-select">
                <Select
                    className="react-select"
                    options={languageOptions}
                    isMulti
                    value={languages}
                    onChange={(selectedOptions) => setLanguages(selectedOptions || [])}
                    placeholder="Type to search languages..."
                    required
                />
                </div>
            </div>
            <div className="mb-1">
                <label className="form-label">Gender *</label>
                <select
                    className="form-select"
                    value={gender}
                    data-testid="create-interpreter-gender-select"
                    onChange={(e) => setGender(e.target.value)}
                    required
                >
                    <option value="" disabled hidden>Select Gender</option>
                    <option value="M">Male</option>
                    <option value="F">Female</option>
                    <option value="O">Other</option>
                    <option value="X">Prefer Not To Say</option>
                </select>
            </div>
            <div className="mb-1">
                <label className="form-label">Address *</label>
                <input
                    className="form-control"
                    type="text"
                    data-testid="create-interpreter-address-input"
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
                    data-testid="create-interpreter-postcode-input"
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
                    data-testid="create-interpreter-phone-number-input"
                    value={phoneNumber}
                    onChange={(e) => setPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Alt Phone Number</label>
                <input
                    className="form-control"
                    type="tel"
                    data-testid="create-interpreter-alternative-phone-number-input"
                    value={altPhoneNumber}
                    onChange={(e) => setAltPhoneNumber(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Notes</label>
                <textarea
                    className="form-control"
                    data-testid="create-interpreter-notes-input"
                    value={notes}
                    onChange={(e) => setNotes(e.target.value)}
                />
            </div>
            <div className="mb-1">
                <label className="form-label">Password *</label>
                <input
                    className="form-control"
                    type="password"
                    data-testid="create-interpreter-password-input"
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
                    data-testid="create-interpreter-confirm-password-input"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    required
                />
            </div>
            {errorElm}
            <button className="btn btn-primary" data-testid="create-interpreter-submit-button" type="submit">Register Interpreter</button>
        </form>
        </>
    )
}

export default CreateInterpreter;