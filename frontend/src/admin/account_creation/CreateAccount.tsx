import CreateAdmin from "./CreateAdmin";
import CreateCustomer from "./CreateCustomer";
import CreateInterpreter from "./CreateInterpreter";

function CreateAccount({ tab }: { tab: "admin" | "interpreter" | "customer" }) {
    return (
        <div>
            <div className="container d-md-flex pt-3 justify-content-between">
                <div className="col-lg-7 col-md-8">
                    {tab === "admin" && <CreateAdmin />}
                    {tab === "interpreter" && <CreateInterpreter />}
                    {tab === "customer" && <CreateCustomer />}
                </div>

                <div className="col-md-3">
                    <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                        * indicates a field is mandatory.
                    </div>
                    <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                        <h5>Or you can...</h5>

                        <hr/>

                        { /* TODO: Alter routing so that these can be made into working links. Currently redirect to home due to 404. */ }

                        <a href="/admin/create-account/admin" className="link-secondary d-block mb-2">Create an Admin</a>
                        <a href="/admin/create-account/interpreter" className="link-secondary d-block mb-2">Create an Interpreter</a>
                        <a href="/admin/create-account/customer" className="link-secondary d-block mb-2">Create a Customer</a>

                        <hr/>
                        
                        <a href="/admin/account-requests" className="link-secondary d-block mb-2">Admin: Account Requests</a>
                        
                        <a href="/admin/profile" className="link-secondary d-block mb-2">Admin: Edit existing User Profiles</a>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default CreateAccount;
