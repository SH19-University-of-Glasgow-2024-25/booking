import apiClient from "../utilities/apiClient";
import { getFieldElements } from "../utilities/FormUtilities";
import { useEffect, useState } from 'react';
import FormEvent from 'react';
import { GenerateErrorDisplayElement } from "../utilities/Error";

interface EditProfileProps {
    user?: string
}

export function EditProfilePage(props: EditProfileProps): JSX.Element {
    return <div className="main-container container">
                {EditProfile(props)}
            </div>;
}

export function EditProfile(props: EditProfileProps): JSX.Element {
    const [editProfile, setEditProfile] = useState<JSX.Element>(
        <div className="main-container container">
            <form id="edit-profile" onSubmit={EditProfileSubmit}>
                <h2>Edit profile</h2>
                <p>Loading...</p>
            </form>
        </div>
    );

    const [userToEdit, setUserToEdit] = useState(props.user || "self");
    const [editProfileErrors, setEditProfileErrors] = useState(<></>);
    const [fieldElms, setFieldElms] = useState<JSX.Element[]>([]);
    const [loadedFlag, setLoadedFlag] = useState(false);

    function EditProfileSubmit(event: FormEvent.FormEvent<HTMLFormElement>) {
        event.preventDefault();

        // getElementById is used as the password fields are returned by getEditFields in a separate file
        // and might not necessarily be present, therefore must be accessed this way.
        if (document.getElementById("edit-profile-confirm-password-container") != undefined) {
            let passwordValue = (document.getElementById("edit-profile-password") as HTMLInputElement).value;
            let passwordConfirmValue = (document.getElementById("edit-profile-confirm-password") as HTMLInputElement).value;
            let passwordConfirmOn = document.getElementById("edit-profile-confirm-password-container")?.classList.contains("confirm-password-on");

            if (passwordConfirmOn && passwordValue != passwordConfirmValue) {
                setEditProfileErrors(GenerateErrorDisplayElement({
                    "error-code": "fail-password-confirm",
                    "error-message": "Your passwords do not match."
                }));
                return;
            }
        }

        let formData = new FormData(event.currentTarget);
        if (formData.get("password") == "") {
            formData.delete("password");
        }

        apiClient.post(`auth/edit_profile`, 
                       formData, {params: {"user": userToEdit}}).then(async response => {
            let edit_response = response.data;
        
            if (edit_response["status"] == "error") {
                setEditProfileErrors(GenerateErrorDisplayElement(edit_response));
            } else {
                let displayElement = <div className="main-container center-container">
                    <div id="edit-profile">
                        Your profile has been successfully edited!
                    </div>
                </div>;

                setEditProfile(displayElement);
            }
        }).catch(err => {
            setEditProfileErrors(GenerateErrorDisplayElement(err.response?.data.error));
        });
    }

    function EditProfileRender() {
        if (loadedFlag)
            setEditProfile(<div>
                <form id="edit-profile" onSubmit={EditProfileSubmit}>
                    { editProfileErrors }

                    { fieldElms }

                    {(fieldElms.length > 0) ? 
                        <button className="btn btn-primary" id="edit-profile-submit" data-testid="edit-profile-submit">Submit</button> : 
                        <p>Unable to find fields for this user type.</p>
                    }
                </form>
            </div>);
    }

    function EditProfileLoad(): Promise<JSX.Element> {
        return new Promise<JSX.Element>((resolve) => {
            apiClient.get("auth/get_user_edit_fields", 
                {params: {"user": userToEdit}}).then(async response => {
                let user_edit_fields_response = response.data;
                if (user_edit_fields_response ["status"] == "error") {
                    resolve(<div className="main-container center-container">
                        { GenerateErrorDisplayElement(user_edit_fields_response) }
                        </div>);
                } else {
                    return user_edit_fields_response;
                }
                
            }).then(async user_edit_fields_response => {
                let fields = user_edit_fields_response.result["fields"];

                let field_elms = await getFieldElements(fields, userToEdit);

                setFieldElms(field_elms);
            }).catch(err => {
                console.log(err);
                resolve(GenerateErrorDisplayElement(err.response?.data.error));
            }).then(() => {
                setLoadedFlag(true);
            });
        });
    }

    useEffect(() => {
        setUserToEdit(props.user || "self")
    }, [props.user]);

    useEffect(() => {
        EditProfileLoad();
    }, [userToEdit]);

    // Use effect call to rerender edit profile when editProfileErrors is called
    useEffect(() => {
        EditProfileRender();
    }, [editProfileErrors, fieldElms]);
    
    return editProfile;
}

export default EditProfile;