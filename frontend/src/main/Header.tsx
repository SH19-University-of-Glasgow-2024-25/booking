import React, { useContext } from 'react';
import '../styles/Header.css';
import { useNavigate } from 'react-router-dom';
import apiClient from '../utilities/apiClient';
import AccountContext from '../utilities/authenticationContext';
import ProtectedContent from '../utilities/ProtectedContent';
import Logo from '/src/assets/logo.svg';

const Header: React.FC = () => {
    const { accountType, setAccountType } = useContext(AccountContext);
    const navigate = useNavigate();

    const handleLogout = () => {
        apiClient.post("/logout/")
            .then(() => {
                navigate('/login');
                setAccountType(null);
            })
            .catch((err) => {
                console.error("Logout Error:", err.response?.data);
            });
    };

    return (
        <>
            <nav className="navbar navbar-expand-lg bg-body-tertiary" data-bs-theme="dark">
                <div className="container">
                    <button onClick={() => navigate('/home')} className="home-button navbar-brand">
                        <img src={Logo} className="logo-image" alt="Logo" />
                    </button>

                    <ProtectedContent key={accountType+"-1"} admin_access customer_access interpreter_access>
                        <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
                            <span className="navbar-toggler-icon"></span>
                        </button>
                    </ProtectedContent>

                    <div className="collapse navbar-collapse" id="navbarSupportedContent">
                    <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li className="nav-item">
                            <ProtectedContent key={accountType} interpreter_access>
                                <a onClick={() => navigate('/appointments')} className="appointments-button nav-link">
                                    Appointments & Translations
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType} customer_access>
                                <a onClick={() => navigate('/appointments')} className="appointments-button nav-link">
                                    Appointments
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType+"1"} admin_access>
                                <a onClick={() => navigate('/appointments')} className="appointments-button nav-link">
                                    Jobs
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType+"2"} customer_access>
                                <a onClick={() => navigate('/translations')} className="translations-button nav-link ">
                                    Translations
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType+"3"} admin_access>
                                <a onClick={() => navigate('/admin')} className="admin-button nav-link ">
                                    Admin
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType+"6"} admin_access customer_access interpreter_access>
                                <a onClick={() => navigate('/profile')} className="admin-button nav-link">
                                    Profile
                                </a>
                            </ProtectedContent>
                        </li>
                        <li className="nav-item">
                            <ProtectedContent key={accountType+"7"} admin_access customer_access interpreter_access>
                                <a onClick={handleLogout} className="logout-button btn btn-outline-success">
                                    Log Out
                                </a>
                            </ProtectedContent>
                        </li>
                    </ul>
                </div>
                </div>
            </nav>
        </>
    );
};

export default Header;
