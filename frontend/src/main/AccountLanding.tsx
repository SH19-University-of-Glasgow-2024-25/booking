import React, { useState, useContext, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import apiClient from '../utilities/apiClient';
import AccountContext from "../utilities/authenticationContext";
import {GenerateErrorDisplayElement} from "../utilities/Error";
import SendPasswordReset from "../utilities/sendPasswordReset";
import { AuthenticationNavBar } from "../utilities/AuthenticationNavBar";

function AccountLanding(props: { registerType: string; }) {

    const { accountType, setAccountType } = useContext(AccountContext);

    const registerType = props.registerType;

    const [email, setEmail] = useState<string>('');
    const [firstName, setFirstName] = useState<string>('');
    const [lastName, setLastName] = useState<string>('');
    const [organisation, setOrganisation] = useState<string>('');

    const [password, setPassword] = useState<string>('');
    const [confirmPassword, setConfirmPassword] = useState<string>('');

    const [address, setAddress] = useState<string>('');
    const [postcode, setPostcode] = useState<string>('');
    const [phoneNumber, setPhoneNumber] = useState<string>('');
    const [altPhoneNumber, setAltPhoneNumber] = useState<string>('');

    const [errorElm, setErrorElm] = useState(<div className="mb-2"></div>);
    const [checkingLoginStatus, setCheckingLoginStatus] = useState<boolean>(true);
    
    const navigate = useNavigate();

    useEffect(() => {
        const checkAuth = async () => {
            try {
                await apiClient.get('/check-auth/')
                .then((res) => {
                    setAccountType(res.data.result.account_type);
                    navigate("/home");
                })
            } catch {
                setCheckingLoginStatus(false);
            }
        };
        
        if (accountType) {
            navigate("/home");
        } else {
            checkAuth();
        }
    }, [])

    const submitCustomerRegistration = (e: React.FormEvent<HTMLFormElement>) => {
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
            address: address,
            postcode: postcode,
            alt_phone_number: altPhoneNumber,
        }
        apiClient.post("/register-customer/", returnData)
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Customer Registration Successful:", res.data);
                    navigate("/verification-email");
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    }

    const handleLogin = (email: string, password: string) => {
        apiClient.post("/login/", { email: email, password: password })
            .then((res) => {
                if (res.data.status == "success") {
                    console.log("Login Successful:", res.data);
                    setAccountType(res.data.result.account_type);
                    navigate("/home");
                } else if (res.data.status == "error") {
                    setErrorElm(GenerateErrorDisplayElement(res.data.error));
                }
            })
            .catch((err) => {
                setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
            });
    };
    
    function submitLogin(e: React.FormEvent<HTMLFormElement>) {
        e.preventDefault();
        handleLogin(email, password);
    }

    const resendEmailVerification = () => {
        navigate("/authentication/resend-email-verification");
    }

    return (
        !checkingLoginStatus &&
        <>
        <AuthenticationNavBar/>
        <div className="main-container container d-md-flex justify-content-center pt-3">
            {registerType === "C" && (
                <form onSubmit={submitCustomerRegistration} className="col-lg-5 col-md-8">
                    <div className="mb-2">
                        <label className="form-label">First Name *</label>
                        <input
                            className="form-control"
                            type="text"
                            value={firstName}
                            data-testid="register-first-name-input"
                            onChange={(e) => setFirstName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Last Name *</label>
                        <input
                            className="form-control"
                            type="text"
                            data-testid="register-last-name-input"
                            value={lastName}
                            onChange={(e) => setLastName(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Organisation *</label>
                        <input
                            className="form-control"
                            type="text"
                            data-testid="register-organisation-input"
                            value={organisation}
                            onChange={(e) => setOrganisation(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Email *</label>
                        <input
                            className="form-control"
                            type="email"
                            data-testid="register-email-input"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Phone Number</label>
                        <input
                            className="form-control"
                            type="tel"
                            data-testid="register-phone-number-input"
                            value={phoneNumber}
                            onChange={(e) => setPhoneNumber(e.target.value)}
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Alt Phone Number</label>
                        <input
                            className="form-control"
                            type="tel"
                            data-testid="register-alt-phone-number-input"
                            value={altPhoneNumber}
                            onChange={(e) => setAltPhoneNumber(e.target.value)}
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Password *</label>
                        <input
                            className="form-control"
                            type="password"
                            data-testid="register-password-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Confirm Password *</label>
                        <input
                            className="form-control"
                            type="password"
                            data-testid="register-confirm-password-input"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Address *</label>
                        <input
                            className="form-control"
                            type="text"
                            data-testid="register-address-input"
                            value={address}
                            onChange={(e) => setAddress(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Postcode *</label>
                        <input
                            className="form-control"
                            type="text"
                            value={postcode}
                            data-testid="register-postcode-input"
                            onChange={(e) => setPostcode(e.target.value)}
                            required
                        />
                    </div>
                    <button 
                        className="btn btn-primary me-3" 
                        type="submit" 
                        data-testid="register-submit-button"
                        >Register Customer
                    </button>
                    <button 
                        className="btn btn-primary" 
                        onClick={() => resendEmailVerification()} 
                        data-testid="resend-email-validation-button"
                        >Resend Verification Email
                    </button>
                    {errorElm}
                </form>
            )}
            {((registerType === "L") || (registerType === "none")) && (
                <form onSubmit={submitLogin} className="col-lg-5 col-md-8">
                    <div className="mb-2">
                        <label className="form-label">Email</label>
                        <input
                            className="form-control"
                            type="email"
                            data-testid="login-email-input"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            required
                        />
                    </div>
                    <div className="mb-2">
                        <label className="form-label">Password</label>
                        <input
                            className="form-control"
                            type="password"
                            data-testid="login-password-input"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            required
                        />
                    </div>
                    <button className="btn btn-primary me-3" id="login-submit-btn" data-testid="login-submit-button" type="submit">Log In</button>
                    <button
                        className="btn btn-primary"
                        type="button"
                        data-testid="forgot-password-button"
                        onClick={() => navigate("/authentication/forgot-password")}
                    >
                        Forgot Password?
                    </button>
                    {errorElm}
                </form>
            )}
            {((registerType === "F")) && (
                <SendPasswordReset/>
            )}
        </div>
        </>
    );    
}

export default AccountLanding;

