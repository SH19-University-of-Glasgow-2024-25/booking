import { render, screen, fireEvent, waitFor } from "@testing-library/react";
import { BrowserRouter, MemoryRouter, Route, Routes } from "react-router-dom";
import AccountLanding from "../main/AccountLanding";
import "@testing-library/jest-dom";
import apiClient from "../utilities/apiClient";
import Verification from "../verification/Verification";
import Landing from "../main/Landing";
import { checkVisible, checkNull } from "../utilities/TestUtilities";

jest.mock("../utilities/apiClient");
const mockPost = jest.fn();
apiClient.post = mockPost;

describe("Account Landing - Unit Tests", () => {

  jest.mock("react-router-dom", () => ({
    ...jest.requireActual("react-router-dom"),
    useNavigate: () => mockNavigate,
  }));
  const mockNavigate = jest.fn();

  const permanentlyVisibleElementIds: string[] = [
    "login-button",
    "request-account-button"
  ];
  
  const loginElementIds: string[] = [
    "login-email-input",
    "login-password-input",
    "login-submit-button"
  ];
  
  const registerElementIds: string[] = [
    "register-first-name-input",
    "register-last-name-input",
    "register-email-input",
    "register-phone-number-input",
    "register-organisation-input",
    "register-alt-phone-number-input",
    "register-password-input",
    "register-confirm-password-input",
    "register-address-input",
    "register-postcode-input",
    "register-submit-button"
  ];
  
  beforeEach(() => {
    render(
      <BrowserRouter>
        <AccountLanding registerType='L'/>
      </BrowserRouter>
    );
    checkVisible(permanentlyVisibleElementIds);
  });

  afterEach(() => {
    checkVisible(permanentlyVisibleElementIds);
  });

  it("GIVEN the user is on the landing page, THEN the login page should be visable", () => {
    checkVisible(loginElementIds);
  });

  it("GIVEN the user is on the landing page, THEN the register page should not be visible", () => {
    checkNull(registerElementIds);
  });
});


describe("Account Landing - Integration Tests", () => {
  beforeEach(() => {
    render(
      <MemoryRouter initialEntries={["/authentication/login"]}>
          <Routes>
            <Route path="/authentication/login" element={<AccountLanding registerType='L'/>} />
            <Route path="/authentication/request-customer" element={<AccountLanding registerType='C'/>} />
            <Route path="/authentication/forgot-password" element={<AccountLanding registerType='F'/>} />
            <Route path="/verification-email" element={<Verification />}/>
            <Route path="/home" element={<Landing/>} />
          </Routes>
      </MemoryRouter>
    );
  })
  
  it("GIVEN the user is on the login page, AND they input the correct details, THEN they should be redirected to home page.", async () => {
    mockPost.mockResolvedValue({
      data: { status: "success", result: { accountType: "A" }},
    });

    fireEvent.change(screen.getByTestId("login-email-input"), { target: { value: process.env.REACT_APP_TEST_EMAIL } });
    fireEvent.change(screen.getByTestId("login-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.click(screen.getByTestId("login-submit-button"));

    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith("/login/", expect.anything());
    });
    
    await waitFor(() => {
      expect(screen.getByText("Home")).toBeInTheDocument();
    });
  });

  it("GIVEN the user is on the login page, AND they input the incorrect details, THEN they should be redirected to home page.", async () => {
    mockPost.mockResolvedValue({
      data: { status: "error", 
        error:{
        "error-message": "Error message.",
        "error-list": ["account-unapproved"],
        "error-code": "explosion",
        },
      }
    });

    fireEvent.change(screen.getByTestId("login-email-input"), { target: { value: process.env.REACT_APP_TEST_EMAIL } });
    fireEvent.change(screen.getByTestId("login-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.click(screen.getByTestId("login-submit-button"));

    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith("/login/", expect.anything());
    });

    await waitFor(() => {
      expect(screen.getByTestId("error-message")).toBeInTheDocument();
    });
  });

  it("GIVEN the user is on the registration page, AND the user has entered valid detaisl in the registration form, WHEN the user submits the registration form, THEN a confirmation message should be displayed ", async () => {
    mockPost.mockResolvedValue({
      data: { status: "success" },
    });
  
    fireEvent.click(screen.getByTestId("request-account-button"));
    // input registration details
    fireEvent.change(screen.getByTestId("register-first-name-input"), { target: { value: "test-first-name" } });
    fireEvent.change(screen.getByTestId("register-last-name-input"), { target: { value: "test-last-name" } });
    fireEvent.change(screen.getByTestId("register-email-input"), { target: { value: "test-email@email.com" } });
    fireEvent.change(screen.getByTestId("register-phone-number-input"), { target: { value: "0123456789" } });
    fireEvent.change(screen.getByTestId("register-alt-phone-number-input"), { target: { value: "" } });
    fireEvent.change(screen.getByTestId("register-organisation-input"), { target: { value: "test-org" } });
    fireEvent.change(screen.getByTestId("register-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.change(screen.getByTestId("register-confirm-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.change(screen.getByTestId("register-address-input"), { target: { value: "test street" } });
    fireEvent.change(screen.getByTestId("register-postcode-input"), { target: { value: "T35T C0D3" } });
  
    fireEvent.click(screen.getByTestId("register-submit-button"));
    await waitFor(() => {
      expect(mockPost).toHaveBeenCalledWith("/register-customer/", expect.anything());
      expect(screen.getByText("A verification email has been sent to your email address.")).toBeInTheDocument();
    });
  });

  it("GIVEN the user is on the registration page, AND the user has entered incorrect detaisl in the registration form, WHEN the user submits the registration form, THEN a confirmation message should be displayed ", async () => {
    mockPost.mockResolvedValue({
      data: { status: "error", 
        error:{
        "error-message": "Error message.",
        "error-list": ["account-unapproved"],
        "error-code": "explosion",
        },
      }
    });
  
    fireEvent.click(screen.getByTestId("request-account-button"));
    // input registration details
    fireEvent.change(screen.getByTestId("register-first-name-input"), { target: { value: "test-first-name" } });
    fireEvent.change(screen.getByTestId("register-last-name-input"), { target: { value: "test-last-name" } });
    fireEvent.change(screen.getByTestId("register-email-input"), { target: { value: "test-email@email.com" } });
    fireEvent.change(screen.getByTestId("register-phone-number-input"), { target: { value: "0123456789" } });
    fireEvent.change(screen.getByTestId("register-alt-phone-number-input"), { target: { value: "" } });
    fireEvent.change(screen.getByTestId("register-organisation-input"), { target: { value: "test-org" } });
    fireEvent.change(screen.getByTestId("register-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.change(screen.getByTestId("register-confirm-password-input"), { target: { value: process.env.REACT_APP_TEST_PASSWORD } });
    fireEvent.change(screen.getByTestId("register-address-input"), { target: { value: "test street" } });
    fireEvent.change(screen.getByTestId("register-postcode-input"), { target: { value: "T35T C0D3" } });
  
    fireEvent.click(screen.getByTestId("register-submit-button"));

    await waitFor(() => expect(mockPost).toHaveBeenCalled());
    
    await waitFor(() => {
      expect(screen.getByTestId("error-message")).toBeInTheDocument();
    });
  });
});
