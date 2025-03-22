import { fireEvent, screen, render, waitFor } from "@testing-library/react";
import "@testing-library/jest-dom";
import apiClient from "../utilities/apiClient";
import { checkVisible, checkNull } from "../utilities/TestUtilities";
import EditProfile from "../profile/EditProfile";
import EditProfileAdmin from "../admin/edit_profile/EditProfileAdmin";

jest.mock("../utilities/apiClient");
const mockPost = jest.fn();
const mockGet = jest.fn();
apiClient.post = mockPost;
apiClient.get = mockGet;

const LANGUAGES = ["language1", "languages2"]

describe("Profile Edit: Test self editing", () => {
    it("GIVEN the user is logged in as an admin THEN they should see the admin fields", async () => {
        mockGet.mockResolvedValue({
            data: {
                status: "success",
                result: {
                    "user-type": "admin",
                    "fields": {
                        "email": "barry@a.com",
                        "password": "",
                        "first_name": "Barry",
                        "last_name": "Jones",
                        "phone_number": "07765123456",
                        "alt_phone_number": null,
                        "notes": null
                    }
                }
            }
        });

        await waitFor(() => {
            render(
                <EditProfile user="self"/>
            );
        });

        await waitFor(() => {
            checkVisible([
                "edit-profile-submit",
                "edit-profile-email",
                "edit-profile-password",
                "edit-profile-fname",
                "edit-profile-lname",
                "edit-profile-tel",
                "edit-profile-tel-alt",
                "edit-profile-notes"
            ]);

            checkNull([
                "edit-profile-organisation",
                "edit-profile-languages",
                "edit-profile-gender",
                "edit-profile-address"
            ]);
        });
    });

    it("GIVEN the user is logged in as an interpreter THEN they should see the interpreter fields", async () => {
        mockGet.mockImplementation(async (url: string) => {
            if (url.includes("get_user_edit_fields")) {
                return {
                    data: {
                        status: "success",
                        result: {
                            "user-type": "interpreter",
                            "fields": {
                                "email": "richard@p.com",
                                "password": "",
                                "first_name": "Richard",
                                "last_name": "Harris",
                                "address": "12 Broadway Avenue",
                                "postcode": "AB13 4DE",
                                "gender": "M",
                                "tag": "",
                                "languages": "",
                                "phone_number": "07765123471",
                                "alt_phone_number": null
                            }
                        }
                    }
                };
            } else if (url.includes("/languages")) {
                return {
                    data: {
                        status: "success",
                        result: {
                            "languages": LANGUAGES
                        }
                    }
                };
            }
        });

        await waitFor(() => {
            render(
                <EditProfile user="self"/>
            );
        });

        await waitFor(() => {
            checkVisible([
                "edit-profile-submit",
                "edit-profile-email",
                "edit-profile-password",
                "edit-profile-fname",
                "edit-profile-lname",
                "edit-profile-address",
                "edit-profile-postcode",
                "edit-profile-tel",
                "edit-profile-tel-alt",
                "edit-profile-languages"
            ]);

            checkNull([
                "edit-profile-organisation",
                "edit-profile-notes"
            ]);
        });
    });

    it("GIVEN the user is logged in as an customer THEN they should see the customer fields", async () => {
        mockGet.mockResolvedValue({
            data: {
                status: "success",
                result: {
                    "user-type": "customer",
                    "fields": {
                        "email": "linda@f.com",
                        "password": "",
                        "first_name": "Linda",
                        "last_name": "Green",
                        "organisation": "The Institute",
                        "address": "123 Elm Street",
                        "postcode": "AB12 3CD",
                        "phone_number": "07765123461",
                        "alt_phone_number": null
                    }
                }
            }
        });

        await waitFor(() => {
            render(
                <EditProfile user="self"/>
            );
        });

        await waitFor(() => {
            checkVisible([
                "edit-profile-submit",
                "edit-profile-email",
                "edit-profile-password",
                "edit-profile-fname",
                "edit-profile-lname",
                "edit-profile-address",
                "edit-profile-postcode",
                "edit-profile-tel",
                "edit-profile-tel-alt"
            ]);

            checkNull([
                "edit-profile-notes",
                "edit-profile-languages"
            ]);
        });
    });
})

describe("Profile Edit: Test admin editing", () => {
    it("GIVEN the user is logged in as an admin THEN they should be able to select richard@p.com and view their fields", async () => {
        mockGet.mockImplementation(async (url: string) => {
            if (url.includes("/emails")) {
                return {
                    data: {
                        status: "success",
                        result: {
                            "admins": [
                                "barry@a.com",
                            ],
                            "interpreters": [
                                "richard@p.com",
                            ],
                            "customers": [
                                "karen@j.com"
                            ]
                        }
                    }
                }
            }
            else if (url.includes("get_user_edit_fields")) {
                return {
                    data: {
                        status: "success",
                        result: {
                            "user-type": "interpreter",
                            "fields": {
                                "email": "richard@p.com",
                                "password": "",
                                "first_name": "Richard",
                                "last_name": "Harris",
                                "address": "12 Broadway Avenue",
                                "postcode": "AB13 4DE",
                                "gender": "M",
                                "tag": "",
                                "languages": "",
                                "phone_number": "07765123471",
                                "alt_phone_number": null,
                                "notes": ""
                            }
                        }
                    }
                };
            } else if (url.includes("/languages")) {
                return {
                    data: {
                        status: "success",
                        result: {
                            "languages": LANGUAGES
                        }
                    }
                };
            }
        });

        await waitFor(() => {
            render(
                <EditProfileAdmin/>
            );
        });

        await waitFor(() => {
            checkVisible(["account-select"])
        });

        fireEvent.change(screen.getByTestId("account-select"), { target: { value: 1 } })
        await waitFor(() => {
            checkVisible([
                "edit-profile-submit",
                "edit-profile-email",
                "edit-profile-password",
                "edit-profile-fname",
                "edit-profile-lname",
                "edit-profile-address",
                "edit-profile-postcode",
                "edit-profile-tel",
                "edit-profile-tel-alt",
                "edit-profile-languages",
                "edit-profile-notes"
            ]);

            checkNull([
                "edit-profile-organisation"
            ]);

            expect(screen.getByText("richard@p.com")).toBeVisible();
        });
    });
});