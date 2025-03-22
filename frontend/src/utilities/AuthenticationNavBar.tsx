import { useNavigate } from "react-router-dom";

export function AuthenticationNavBar() {
    const navigate = useNavigate();

    return <>
    <div className="navbar navbar-expand-lg bg-body-tertiary green-texture" data-bs-theme="dark">
        <div className="container">
            <div className="navbar-brand">
                Authentication
            </div>
            <div className="mb-2">
                <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
                    <li className="nav-item">
                        <a
                            className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75"
                            id="request-btn"
                            data-testid="request-account-button"
                            onClick={() => navigate("/authentication/request-customer")}
                        >
                            Request Customer Account
                        </a>
                    </li>
                    <li className="nav-item">
                        <a
                            className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75"
                            id="login-btn"
                            data-testid="login-button"
                            onClick={() => navigate("/authentication/login")}
                        >
                            Login
                        </a>
                        </li>
                </ul>
            </div>
        </div>
    </div>
    </>;
}