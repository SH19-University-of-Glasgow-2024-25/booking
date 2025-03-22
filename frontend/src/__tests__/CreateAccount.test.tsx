import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter, MemoryRouter, Route, Routes } from "react-router-dom";
import "@testing-library/jest-dom";
import apiClient from "../utilities/apiClient";
import Verification from "../verification/Verification";
import Landing from "../main/Landing";
import AccountContext from "../utilities/authenticationContext";
import AdminPage from "../admin/Admin";
import { checkNull, checkVisible } from "../utilities/TestUtilities";

jest.mock("../utilities/apiClient");
const mockPost = jest.fn();
const mockGet = jest.fn();

apiClient.post = mockPost;
apiClient.get = mockGet;

mockPost.mockResolvedValue({
    data: { status: "success", result: { customers: {} } },
});

// this is required to succesfuly load the admin page in both sets of tests below
mockGet.mockResolvedValue({
    data:
    {
        status: "success",
        result: {
            customers: [
                {
                    first_name: "test_first_name",
                    last_name: "test_last_name",
                    organisation: "test_organisation",
                    email: "test@test.com",
                    phone_number: "07765123469",
                    address: "test street lane",
                    postcode: "T35T GB"
                }
            ]
        }
    },
});

const createAdminFormElementIds: string[] = [
    "create-admin-first-name-input",
    "create-admin-last-name-input",
    "create-admin-email-input",
    "create-admin-phone-number-input",
    "create-admin-alternative-phone-number-input",
    "create-admin-notes-input",
    "create-admin-password-input",
    "create-admin-confirm-password-input",
    "create-admin-submit-button"
];
const createInterpreterFormElementIds: string[] = [
    "create-interpreter-first-name-input",
    "create-interpreter-last-name-input",
    "create-interpreter-email-input",
    "create-interpreter-language-select",
    "create-interpreter-gender-select",
    "create-interpreter-address-input",
    "create-interpreter-postcode-input",
    "create-interpreter-phone-number-input",
    "create-interpreter-alternative-phone-number-input",
    "create-interpreter-notes-input",
    "create-interpreter-password-input",
    "create-interpreter-confirm-password-input",
    "create-interpreter-submit-button"
];

const createCustomerFormElementIds: string[] = [
    "create-customer-first-name-input",
    "create-customer-last-name-input",
    "create-customer-organisation-input",
    "create-customer-email-input",
    "create-customer-address-input",
    "create-customer-postcode-input",
    "create-customer-phone-number-input",
    "create-customer-alternative-phone-number-input",
    "create-customer-notes-input",
    "create-customer-password-input",
    "create-customer-confirm-password-input",
    "create-customer-submit-button"
];

describe("Admin Page - Unit Tests", () => {
    beforeEach(async () => {
        await waitFor(() => {
            render(
                <AccountContext.Provider value={{ accountType: "A", setAccountType: jest.fn() }}>
                    <BrowserRouter>
                        <AdminPage />
                    </BrowserRouter>
                </AccountContext.Provider>
            );
        });
    });

    it("GIVEN the user is on the admin page AND they have click the account request button THEN customer requests should be visible AND no form elements should be visible", async () => {
        fireEvent.click(screen.getByTestId("admin-request-feed-button"));
        await waitFor(() => {
            expect(screen.getByText((content) => content.includes("test_first_name"))).toBeVisible();
            expect(screen.getByText((content) => content.includes("test street lane"))).toBeVisible();
        });
        checkNull([...createAdminFormElementIds, ...createCustomerFormElementIds, ...createInterpreterFormElementIds]);
    });

    it("GIVEN the user is on the create admin form THEN the form should be well formed and visible", async () => {

        fireEvent.click(screen.getByTestId("admin-create-admin-button"));
        await waitFor(() => {
            checkVisible(createAdminFormElementIds);
        });

    });

    it("GIVEN the user is on the create interpreter form THEN the form should be well formed and visible", async () => {
        const mockGetSuccessResponse = {
            data: {
                status: "success",
                result: {
                    languages: [
                        { value: "english", label: "English" },
                        { value: "spanish", label: "Spanish" },
                        { value: "french", label: "French" },
                    ],
                },
            },
        };

        mockGet.mockResolvedValue(mockGetSuccessResponse);
        fireEvent.click(screen.getByTestId("admin-create-interpreter-button"));
        await waitFor(() => {
            checkVisible(createInterpreterFormElementIds);
        });
    });

    it("GIVEN the user is on the create customer form THEN the form should be well formed and visible", async () => {
        fireEvent.click(screen.getByTestId("admin-create-customer-button"));
        await waitFor(() => {
            checkVisible(createCustomerFormElementIds);
        });
    });
});

jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockNavigate,
}));
const mockNavigate = jest.fn();

describe("Admin Page - Integration Tests", () => {
    beforeEach(async () => {
        await waitFor(() => {
            render(
                <AccountContext.Provider value={{ accountType: "A", setAccountType: jest.fn() }}>
                    <MemoryRouter initialEntries={["/admin"]}>
                        <Routes>
                            <Route path="/admin" element={<AdminPage />} />
                            <Route path="/verification-email" element={<Verification />} />
                            <Route path="/home" element={<Landing />} />
                        </Routes>
                    </MemoryRouter>
                </AccountContext.Provider>
            );
        });
    });

    it("GIVEN the admin is on the create admin screen AND they input the correct details THEN a success page should be displayed", async () => {
        fireEvent.click(screen.getByTestId("admin-create-admin-button"));
        await waitFor(() => {
            expect(screen.getByRole("heading", { level: 3, name: "Create Admin" })).toBeInTheDocument();
        });
        fireEvent.change(screen.getByTestId("create-admin-first-name-input"), { target: { value: "test-first-name" } });
        fireEvent.change(screen.getByTestId("create-admin-last-name-input"), { target: { value: "test-last-name" } });
        fireEvent.change(screen.getByTestId("create-admin-email-input"), { target: { value: "test-email@email.com" } });
        fireEvent.change(screen.getByTestId("create-admin-phone-number-input"), { target: { value: "0123456789" } });
        fireEvent.change(screen.getByTestId("create-admin-alternative-phone-number-input"), { target: { value: "" } });
        fireEvent.change(screen.getByTestId("create-admin-notes-input"), { target: { value: "test-org" } });
        fireEvent.change(screen.getByTestId("create-admin-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
        fireEvent.change(screen.getByTestId("create-admin-confirm-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
        fireEvent.click(screen.getByTestId("create-admin-submit-button"));
        await waitFor(() => {
            expect(screen.getByTestId("account-creation-success")).toBeInTheDocument();
        });
    });

    // TODO: the test fails as we cannot interact with the select options "language" and "gender" correctly
    // it("GIVEN the admin is on the create interpreter screen AND they input the correct details THEN a success page should be displayed", async () => {
    //     const mockGetSuccessResponse = {
    //         data: {
    //             status: "success",
    //             result: {
    //                 languages: [
    //                     { value: "english", label: "English" },
    //                     { value: "spanish", label: "Spanish" },
    //                     { value: "french", label: "French" },
    //                 ],
    //             },
    //         },
    //     };

    //     mockGet.mockResolvedValue(mockGetSuccessResponse);
    //     fireEvent.click(screen.getByTestId("admin-create-interpreter-button"));
    //     await waitFor(() => {
    //         expect(screen.getByRole("heading", { level: 1, name: "Interpreter" })).toBeInTheDocument();
    //     });
    //     fireEvent.change(screen.getByTestId("create-interpreter-first-name-input"), { target: { value: "test-first-name" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-last-name-input"), { target: { value: "test-last-name" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-email-input"), { target: { value: "test@emai.com" } });
    //     // const selectWrapper = screen.getByTestId("create-interpreter-language-select");
    //     // const languageInput = within(selectWrapper).getByRole("combobox");

    //     // const selectWrapper = screen.getByTestId("create-interpreter-language-select");

    //     // // Click to open dropdown
    //     // await userEvent.click(selectWrapper);

    //     // // Type "English" into the input field
    //     // await userEvent.type(selectWrapper, "English");

    //     // // Press Enter to select it
    //     // await userEvent.keyboard("{Enter}"); 

    //     // fireEvent.click(screen.getByTestId("create-interpreter-gender-select"));
    //     // fireEvent.click(screen.getByText("Male"));
    //     fireEvent.change(screen.getByTestId("create-interpreter-address-input"), { target: { value: "test address lane" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-postcode-input"), { target: { value: "T35T GB" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-phone-number-input"), { target: { value: "0123456789" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-alternative-phone-number-input"), { target: { value: "" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-notes-input"), { target: { value: "test-org" } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    //     fireEvent.change(screen.getByTestId("create-interpreter-confirm-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    //     fireEvent.click(screen.getByTestId("create-interpreter-submit-button"));
    //     screen.debug();
    //     await waitFor(() => {
    //         expect(screen.getByTestId("account-creation-success")).toBeInTheDocument();
    //     });

    // });

    it("GIVEN the admin is on the create admin screen AND they input the correct details THEN a success page should be displayed", async () => {
        fireEvent.click(screen.getByTestId("admin-create-customer-button"));
        await waitFor(() => {
            expect(screen.getByRole("heading", { level: 3, name: "Create Customer" })).toBeInTheDocument();
        });
        fireEvent.change(screen.getByTestId("create-customer-first-name-input"), { target: { value: "test-first-name" } });
        fireEvent.change(screen.getByTestId("create-customer-last-name-input"), { target: { value: "test-last-name" } });
        fireEvent.change(screen.getByTestId("create-customer-organisation-input"), { target: { value: "test organisation" } });
        fireEvent.change(screen.getByTestId("create-customer-email-input"), { target: { value: "test-email@email.com" } });
        fireEvent.change(screen.getByTestId("create-customer-address-input"), { target: { value: "test address lane" } });
        fireEvent.change(screen.getByTestId("create-customer-postcode-input"), { target: { value: "T35T GB" } });
        fireEvent.change(screen.getByTestId("create-customer-phone-number-input"), { target: { value: "0123456789" } });
        fireEvent.change(screen.getByTestId("create-customer-alternative-phone-number-input"), { target: { value: "" } });
        fireEvent.change(screen.getByTestId("create-customer-notes-input"), { target: { value: "test-org" } });
        fireEvent.change(screen.getByTestId("create-customer-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
        fireEvent.change(screen.getByTestId("create-customer-confirm-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
        fireEvent.click(screen.getByTestId("create-customer-submit-button"));
        await waitFor(() => {
            expect(screen.getByTestId("account-creation-success")).toBeInTheDocument();
        });
    });

});
