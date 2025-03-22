import React, { useState } from "react";
import apiClient from "../utilities/apiClient";
import { useNavigate } from "react-router-dom";
import {GenerateErrorDisplayElement} from "../utilities/Error";
import { AuthenticationNavBar } from "../utilities/AuthenticationNavBar";

function ResendVerification() {
    const [email, setEmail] = useState<string>('');
    const [errorElement, setErrorElement] = useState(<div className="mb-2"></div>);
    const navigate = useNavigate();

    const resendVerificationEmail = (e: React.FormEvent<HTMLFormElement>) => {
        e.preventDefault();

        apiClient.post("/resend-email-verification/", {email: email})
            .then((response) => {
                if (response.data.status == "success") {
                    navigate("/verification-email/");
                } else if (response.data.status == "error") {
                    setErrorElement(GenerateErrorDisplayElement(response.data.error));
                }
            })
            .catch((error) => {
                setErrorElement(GenerateErrorDisplayElement(error.response?.data.error));
            })
    }

    return(
        <>
        <AuthenticationNavBar/>
        <div className="main-container container d-md-flex justify-content-center pt-3">
            <form onSubmit={resendVerificationEmail} className="col-lg-5 col-md-8">
                <div className="mb-2"> 
                    <h3>Resend email verification</h3>
                    <label className="form-label">Email</label>
                    <input 
                        className="form-control"
                        type="email"
                        data-testid="resend-email-verification-email-input"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <button 
                    className="btn btn-primary me-3"
                    data-testid="resend-email-verification-submit-button"
                    type="submit"
                >
                    Send Email
                </button>
                {errorElement}
            </form>
        </div>
        </>
    )
}

export default ResendVerification;