import React, { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import apiClient from './apiClient';
import { GenerateErrorDisplayElement } from './Error';

const NewPassword: React.FC = () => {
    const { uidb64, token } = useParams<{ uidb64: string; token: string }>();
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [errorElm, setErrorElm] = useState(<div></div>);
    const navigate = useNavigate();

    const clearForm = () => {
        setPassword('');
        setConfirmPassword('');
    }


    const handleSubmit = (event: React.FormEvent) => {
        event.preventDefault();
        if (password !== confirmPassword) {
            setErrorElm(<div>Passwords do not match</div>);
            return;
        }

        const returnData = {
            uidb64,
            token,
            password,
        };

        apiClient.post('/update-password/', returnData)
            .then((res) => {
                if (res.data.status === 'success') {
                    console.log('Password updated successfully');
                    navigate('/login');
                    clearForm()
                } else {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
                console.error('Failed to update password:', err);
            });
    };

    return (
        <div>
            <h2>Update Password</h2>
            <form onSubmit={handleSubmit}>
                <label>
                    New Password:
                    <input
                        type="password"
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                        required
                    />
                </label>
                <label>
                    Confirm Password:
                    <input
                        type="password"
                        value={confirmPassword}
                        onChange={(e) => setConfirmPassword(e.target.value)}
                        required
                    />
                </label>
                <button className="btn btn-primary" type="submit">Update Password</button>
                {errorElm}
            </form>
        </div>
    );
};

export default NewPassword;
