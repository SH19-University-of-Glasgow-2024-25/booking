import React from 'react';
import apiClient from "../utilities/apiClient";
import Select from 'react-select';


export async function getFieldElements(fields: { [s: string]: string; }, userToEdit: string): Promise<(JSX.Element)[]> {
    let existingPasswordField = <></>;
    if (userToEdit == "self") {
        existingPasswordField = <>
            <label className="form-label">Your existing password:</label> <input className="form-control" type="password" id="edit-profile-existing-password" name="existing_password" autoComplete="new-password"></input>
        </>;
    }
    
    let possible_fields = new Map<string, JSX.Element>(Object.entries({
        "email": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Email:</label> <input className="form-control" type="email" data-testid="edit-profile-email" id="edit-profile-email" name="email" defaultValue={fields["email"]}></input>
        </div>,
        "password": <div className="edit-profile-password-pair mb-1">
            <div className="edit-profile-input-line mb-1">
                <label className="form-label">New Password:</label> 
                <input className="form-control" type="password" id="edit-profile-password" data-testid="edit-profile-password" name="password" autoComplete="new-password"
                    onKeyDown={() => {
                        if (userToEdit == "self") {
                            let elm = document.getElementById("edit-profile-confirm-password-container");
                            if (elm?.classList.contains("confirm-password-off"))
                                elm?.classList.remove("confirm-password-off");
                            if (!elm?.classList.contains("confirm-password-on"))
                                elm?.classList.add("confirm-password-on");
                        }
                    }}> 
                </input>
            </div>
            <div className="edit-profile-input-line confirm-password-off mb-1" id="edit-profile-confirm-password-container">
                <label className="form-label">Confirm New Password:</label> <input className="form-control" type="password" id="edit-profile-confirm-password" data-testid="edit-profile-confirm-password" autoComplete="new-password" name="confirm_password"></input>
                {existingPasswordField}
            </div>
        </div>,
        "first_name": <div className="edit-profile-input-line mb-1">
            <label className="form-label">First name:</label> <input className="form-control" type="text" id="edit-profile-fname" data-testid="edit-profile-fname" name="first_name" defaultValue={fields["first_name"]}></input>
        </div>,
        "last_name": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Last name:</label> <input className="form-control" type="text" id="edit-profile-lname" data-testid="edit-profile-lname" name="last_name" defaultValue={fields["last_name"]}></input>
        </div>,
        "organisation":<div className="edit-profile-input-line mb-1">
            <label className="form-label">Organisation:</label> <input className="form-control" type="text" id="edit-profile-organisation" data-testid="edit-profile-organisation" name="organisation" defaultValue={fields["organisation"]}></input>
        </div>,
        "phone_number": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Phone number:</label> <input className="form-control" type="tel" id="edit-profile-tel" data-testid="edit-profile-tel" name="phone_number" defaultValue={fields["phone_number"]}></input>
        </div>,
        "alt_phone_number": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Alternate phone number:</label> <input className="form-control" type="tel" id="edit-profile-tel-alt" data-testid="edit-profile-tel-alt" name="alt_phone_number" defaultValue={fields["alt_phone_number"]}></input>
        </div>,
        "address": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Address:</label> <input className="form-control" type="text" id="edit-profile-address" data-testid="edit-profile-address" name="address" defaultValue={fields["address"]}></input>
        </div>,
        "postcode": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Postcode:</label> <input className="form-control" type="text" id="edit-profile-postcode" data-testid="edit-profile-postcode" name="postcode" defaultValue={fields["postcode"]}></input>
        </div>,
        "gender": <div className="edit-profile-input-line mb-1">
        <label className="form-label">Gender: </label> 
            <select className="form-select" id="edit-profile-gender" data-testid="edit-profile-gender" name="gender" defaultValue={fields["gender"]}>
                <option value="X">Prefer not to say</option>
                <option value="M">Male</option>
                <option value="F">Female</option>
                <option value="O">Other</option>
            </select>
        </div>,
        "notes": <div className="edit-profile-input-line mb-1">
            <label className="form-label">Notes: </label> 
            <textarea className="form-control" name="notes" rows={5} defaultValue={fields["notes"]} id="edit-profile-notes" data-testid="edit-profile-notes"></textarea>
        </div>
    }));

    // Add languages to possible_fields if languages is a field for this user.
    // This is separate from the possible_fields creation above
    // as the Select element requires the data from the /languages API call
    // and creating there and then rerendering later does not work properly.
    if (Object.keys(fields).includes("languages")) {
        await apiClient.get("/languages/")
        .then((res) => {
            if (res.data.status == "success") {
                console.log("Language Retrieval Successful:", res.data);
                const formattedOptions = res.data.result.languages.map((lang:string) => ({
                    value: lang,
                    label: lang,
                }));
                possible_fields.set("languages",
                    <div className="edit-profile-input-line mb-1" data-testid="edit-profile-languages">
                    <label className="form-label">Languages: </label> <Select
                            className="react-select"
                            options={formattedOptions}
                            isMulti
                            placeholder="Type to search languages..."
                            id="edit-profile-languages"
                        />
                </div>
                );
            }
        });
    }

    let i = 0;
    let fields_elms: (JSX.Element)[] = Object.entries(fields).map(([field_name]) => {
        i++;
        let field = () => possible_fields.get(field_name);
        if (field != undefined)
            return React.createElement(field, {key: i});
    }).filter(item => item !== undefined);

    return fields_elms;
}