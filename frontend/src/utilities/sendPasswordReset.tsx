import React, { useState } from 'react';
import apiClient from "../utilities/apiClient";
import {GenerateErrorDisplayElement} from "../utilities/Error";

const SendPasswordReset: React.FC = () => {
    const [email, setEmail] = useState('');
    const [message, setMessage] = useState('');
    const [errorElm, setErrorElm] = useState(<div></div>);

    const clearForm = () => {
        setEmail('');
    }

    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        const returnData = {
            email: email,
        }
        apiClient.post("/send-password-reset-email/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log('Password reset email sent to:', email);
                    setMessage('Password reset email sent successfully.');
                    setErrorElm(<div></div>);
                    clearForm();
                } else {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                    setMessage('');
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
                console.error('Failed to send password reset email:', err);
            });
        clearForm()
    };

    return (
        <div id="forgot-pass-email">
            <h3>Reset Password</h3>
            <form onSubmit={handleSubmit}>
                <div className="mb-3">
                <label className="form-label">Email:</label>
                    <input
                        className="form-control"
                        type="email"
                        value={email}
                        onChange={(e) => setEmail(e.target.value)}
                        required
                    />
                </div>
                <button className="btn btn-primary mb-3" type="submit">Send Reset Email</button>
                {message && <p className='email-text'>{message}</p>}
                {errorElm}
                <p className='email-text'>If your email exists in our database you should receive an email. Check your spam folder!</p>
            </form>
        </div>
    );
};

export default SendPasswordReset;