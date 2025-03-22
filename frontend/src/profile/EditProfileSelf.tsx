import ProtectedContent from "../utilities/ProtectedContent";
import EditProfile from "./EditProfile";

export function EditProfileSelf(): JSX.Element {

    return <>
        <div className="navbar green-texture" data-bs-theme="dark">
            <div className="container">
                <div className="navbar-inner">
                    <div className="navbar-brand">
                        Edit your profile
                    </div>
                </div>
            </div>
        </div>

        <div className="main-container container d-md-flex justify-content-between">
            <div className="col-lg-7 col-md-8">
                <h3>Edit your profile:</h3>
                <EditProfile/>
            </div>

            
            <div className="col-md-3">
                <ProtectedContent interpreter_access>
                    <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2 border-warning">
                        <h5>Remember...</h5>
                        Set and update your languages so that you can be assigned to the right appointments.
                    </div>
                </ProtectedContent>

                <ProtectedContent admin_access>
                    <div className="px-3 pt-2 ms-4 border-start bg-body-tertiary mt-3 pb-2">
                        <h5>Or you can...</h5>

                        { /* TODO: Alter routing so that these can be made into working links. Currently redirect to home due to 404. */ }
                        
                        <a href="/admin/profile" className="link-secondary">Admin: Edit other user&apos;s profiles</a>
                    </div>
                </ProtectedContent>
            </div>
            
        </div>
    </>;
}