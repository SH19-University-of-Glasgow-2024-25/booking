# Dev Guide: Front-End

## Overview

This project's frontend uses the React library alongside the build tool Vite. Initially we chose to use TypeScript on top of this as in the long run this is generally a more maintainable approach.
Alongside this the project follows best practices for maintainability by utilising technologies such as ESLint for the linting, and Babel and Jest for the frontend testing. Also as well as the obvious html and css found sitewide, Bootstrap has also been implemented to stream line the design process.

To start the development server when docker is not being used run the following commands:

```
npm install # Install dependencies
npm run dev # Start the dev server
# Use one or the other, not both!
npm run build # Used to create a producton-ready build
```

## Project Structure

The codebase itself follows a fairly modular structure, within the root in the top directory you will find config files for the linter and jest, these just ensure the relevant features are working appropriately and also pointing in the correct direction.

```
/frontend
├── public/             # Static assets (favicons, logos, etc.)
├── src/                # Source code
│   ├── admin/          # Admin-related components & logic
│   ├── appointments/   # Appointment-related components
│   ├── assets/         # Images, icons, textures
│   ├── main/           # Core UI components (Header, Footer, Landing)
│   ├── profile/        # User profile management
│   ├── translations/   # Translation & language-related logic
│   ├── utilities/      # Helper functions (API calls, authentication, etc.)
│   ├── verification/   # User verification-related components
│   ├── __tests__/      # Unit & integration tests
│   ├── styles/         # CSS stylesheets
│   └── setupTests.js   # Test configuration
├── coverage/           # Test coverage reports (auto-generated)
├── package.json        # Project dependencies & scripts
├── vite.config.ts      # Vite configuration file
├── tsconfig.json       # TypeScript configuration
├── Dockerfile          # Container setup for deployment
├── jest.config.js      # Jest testing configuration
└── README.md           # Project documentation
```

### Key Folders and Files

`node_modules/`: Contains all installed dependencies. This folder was auto generated upon `npm install` at the beginning of the project. **Do not modify this manually**.\
`package.json`: Defines these project dependencies, also version numbers.\
`package-lock.json`: Ensures that the same versions are installed across different environments, preventing unexpected/unwanted version updates.\
`src/__tests__/`: This folder contains all unit and integration tests for the frontend.\
`src/admin/`: This folder contains the main admin component as well as admin exclusive features such as **account_creation/requests** and **edit_profile**, other admin components are found elsewhere but they are generally closely related to the folder name.\
`src/assets/`: Contains all of our static files that are used site-wide these can be textures, company images, logos, etc.\
`src/main/`: Main contains the core components such as the main landing the actual `App.tsx` and `main.tsx` and the header and footer components, everything else is linked from these core components.\
`src/styles/`: Although Bootstrap is used throughout on components there is still directory featuring any other .css files\
`src/utilities`: Components that can be used throughout for a particular job are found here these include a Password Reset component, `sendPasswordReset.tsx`. The commonly appearing error component, `Error.tsx`. There are also other components with more particular use cases.

All other files and directories are fairly self-explantory and contain what they say on the box, generally corresponding to a particular feature or component on the site.

### Environment Variables (.env)

For security purposes ensure that the .env.dev file always remains in the .gitignore as the variables contained within this file should never be committed to version control - .env.dev should be manualy loaded into the application.
This is because the project uses environment variables to configure database connections, authentication, and API settings.
- Also useful to note that different `.env` files should be used for different environments, there is only a .env.dev in our current project, but good practice would be to create a .env.prod for production for example.
The environment variables required for this project are as follows:
- VITE_APP_BASE_URL //base URL for axios API client
- REACT_APP_TEST_EMAIL //for frontend tests
- REACT_APP_TEST_PASSWORD //for frontend tests
## API Guide

All API responses follow a set format so that errors can easily be detected and error information displayed. `bookingandbilling.utilities` provides `APIresponse` and `ErrorResponse` classes that inherit from and replace the use of the standard REST framework `Response` class to enforce this format.

### API Response Format

```
{
   "status": "error" / "success",
IF NOT ERROR:
   "result": { ... Normal response data...},
ELSE IF ERROR:
    "error": {
        "error-code": "some-error-code"
        "error-http-code": 400 etc,
        "error-message": "User friendly error message",
        "error-data": { ... optional additional error data for use by the frontend ...}
        "error-list": ["optional list of", "errors", "for example for errors returned", "by a serialiser"]
    }
}
```

### Frontend Usage

In order to communicate with backend...

Import the API client and error display function:

```ts
import {GenerateErrorDisplayElement} from "./utilities/Error";
import apiClient from './utilities/apiClient';
```

Set up an error element for displaying errors:

```ts
const [errorElm, setErrorElm] = useState(<div></div>);
```

Place that element in some visible place in your HTML, for example:
```html
...
    <button type="submit">Log In</button>
    {errorElm}
</form>
...
```

Make your requests in the following way:
```ts
apiClient.get("/whatever-endpoint")
    .then((res) => {
        if (res.data.status == "success") {
            // Do stuff with res.data.result!!
        } else if (res.data.status == "error") {
            setErrorElm(GenerateErrorDisplayElement(res.data.error));
        }
    })
    .catch((err) => {
        setErrorElm(GenerateErrorDisplayElement(err.response?.data.error));
    });
```

## How To...(API)

### Call an API Endpoint
In `frontend/src/utilities/apiClient.tsx` an instance of axios (an API client) is created with our required settings. All API calls should be made using this instance. This can be accessed on a page similarly to (if not exactly like) this `import apiClient from './utilities/apiClient';`.

An API endpoint will need to have been made as desired and included in `backend/bookingandbilling/urls.py`. This can then be called as follows: `apiClient.post("/register/", returnData)`, where `post` can be replaced by `get`, `/register/` can be replaced by any endpoint url, and `returnData` is a dictionary containing the required post values (or be ommitted entirely if not needed - ie get).

### Make API Endpoints Require / Not Require Login
All API Endpoints require the request to contain a valid authToken by default - which is automatically handled by the API client if it exists. To allow access to non authenticated users / calls put `permission_classes = [AllowAny]` at the top of the endpoint.

### Check the User Type calling an Endpoint
The request authToken can be got using `request.COOKIES.get('authToken')`. From this, the associated `User` model can be accessed using `get_user_from_token(token)` which returns None if token is None or an associated user is not found. The user returned is of the base `User` model. To retrieve the high-level user and learn it's type, you can use `user, type = get_full_user(user)` which returns the high-level user type (of type Admin, Interpreter or Customer) and the type as an AccountType ENUM value.

### Restrict an API to specific user types
There is a custom permission class that can be used to restrict APIs to specific user types. To use it include `permission_classes = [lambda : IsUserType(allowed_types=[AccountType.ADMIN, AccountType.CUSTOMER])]` at the top of the endpoint - where the `allowed_types` list can contain any AccountType ENUM values. This will allow only users of a type listed to access the endpoint.

### Restrict Access to Pages
The `frontend/src/utilities/ProtectedRoute.tsx` component can be wrapped around other React components. It has three boolean properties which determine which user types can access the page. By default no account types are allowed so they must be specified. While this can be used anywhere, I do not see it being used outside of `App.tsx`. It is imported as `import ProtectedRoute from './utilities/ProtectedRoute';` and used as `<ProtectedRoute admin_access customer_access interpreter_access><PageToBeProtected /></ProtectedRoute>` where the `*_access` properties specify the allowed user types and the middle component is the protected content / page. Examples of this can be found in `App.tsx`. If a disallowed account type tries to access one of these pages they will be returned to the login page.

### Restrict Access to Specific Page Content
The `frontend/src/utilities/ProtectedComponent.tsx` component can be wrapped around other React components. It is imported as `import ProtectedComponent from './utilities/ProtectedComponent';` and used identically to the `ProtectedRoute` component described above. If a disallowed account type tries to load the page content nothing is rendered.

## ESLint Configuration

This project follows ESLint rules to enforce code quality and consistency. Type-aware linting is recommended for better TypeScript support.

### Updating ESLint for Type Checking

If you need stricter linting rules, update the top-level `parserOptions`
- Configure the top-level `parserOptions` property like this:

```js
export default tseslint.config({
  languageOptions: {
    // other options...
    parserOptions: {
      project: ['./tsconfig.node.json', './tsconfig.app.json'],
      tsconfigRootDir: import.meta.dirname,
    },
  },
})
```

Replace `tseslint.configs.recommended` with one of the following for stricter rules:
- `tseslint.configs.recommendedTypeChecked`
- `tseslint.configs.strictTypeChecked`
- Optionally, `...tseslint.configs.stylisticTypeChecked` for stylistic consistency.

## Testing with Jest

Jest is used for unit and integration testing. The testing setup includes:
- React component test using `@testing-library/react`
- Mocking functions with `jest.fn()`
- Snapshot testing for UI components

### Running Tests

To run all tests:
```
npm test
```
To run tests in watch mode:
```
npm test -- --watch
```
To generate a test coverage report:
```
npm test -- --coverage
```

## Additional Notes

When not using docker we often had problems that always came back to not properly installing all dependencies, so if the docker is not being used ensure to:
```
npm install
```

You might find that the linter is a bit strict and sometimes has bugs with line breaks and white space, but it is nowhere near how strict flake8 in the backend is. Nothing gets past flake8...

This guide aims to provide a smooth handover to the client, ensuring they can easilty continue development and maintenance of the system.

