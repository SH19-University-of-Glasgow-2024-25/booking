import { useState } from "react";
import RequestAccept from "./account_requests/RequestAccept";
import CreateAccount from "./account_creation/CreateAccount";
import EditProfileAdminPage from "./edit_profile/EditProfileAdmin";

function AdminPage() {
    const [tab, setTab] = useState<"request" | "create" | "profiles">("request");
    const [creating, setCreating] = useState<"admin" | "interpreter" | "customer">("admin");

    const toggleTab = (tab: "request" | "create" | "profiles") => {
        setTab(tab);
    };

    return (
        <>
        <div className="navbar navbar-expand-lg bg-body-tertiary green-texture" data-bs-theme="dark">
            <div className="container">
                <div className="navbar-brand">
                    Admin
                </div>
                <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbar-collapse-2">
                    <span className="navbar-toggler-icon"></span>
                </button>
                <div className="collapse navbar-collapse" id="navbar-collapse-2">
                    <ul className="navbar-nav ms-auto mb-2 mb-lg-0">
                        <li className="nav-item">
                            <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" data-testid="admin-request-feed-button" onClick={() => toggleTab("request")}>
                                Account Requests
                            </button>
                        </li>
                        <li className="nav-item dropdown">
                            <a className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" role="button" data-bs-toggle="dropdown">
                                Create Accounts
                            </a>
                            <ul className="dropdown-menu green-texture border-x">
                                <a className="dropdown-item" data-testid="admin-create-admin-button" onClick={() => { setCreating("admin"); toggleTab("create"); }}>Admin</a>
                                <a className="dropdown-item" data-testid="admin-create-interpreter-button" onClick={() => { setCreating("interpreter"); toggleTab("create"); }}>Interpreter</a>
                                <a className="dropdown-item" data-testid="admin-create-customer-button" onClick={() => { setCreating("customer"); toggleTab("create"); }}>Customer</a>
                            </ul>
                        </li>
                        <li className="nav-item">
                            <button className="btn btn-link link-light link-underline-light link-offset-2 link-underline-opacity-75" onClick={() => toggleTab("profiles")}>
                                Edit user profiles
                            </button>
                        </li>
                    </ul>
                </div>
            </div>
        </div>
            {tab === "request" && <RequestAccept />}
            {tab === "create" && <CreateAccount tab={creating} />}
            {tab === "profiles" && <EditProfileAdminPage/>}
        </>
    );
}

export default AdminPage;
