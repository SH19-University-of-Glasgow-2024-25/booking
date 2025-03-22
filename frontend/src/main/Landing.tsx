import ProtectedContent from '../utilities/ProtectedContent';
import { useContext } from 'react';
import AccountContext from '../utilities/authenticationContext';
import { Navigate } from 'react-router-dom';

function Landing(){
    const { accountType } = useContext(AccountContext);

    if (accountType == "A")
      return <Navigate to="/admin" replace />;
    else if (accountType == "I")
      return <Navigate to="/appointments" replace />;
    else if (accountType == "C")
      return <Navigate to="/appointments" replace />;

    return (
    <>
    <div className="navbar green-texture" data-bs-theme="dark">
        <div className="container">
          <div className="navbar-inner">
              <div className="navbar-brand">
                  Home
              </div>
          </div>
        </div>
      </div>

    <div className="main-container container">
        <ProtectedContent admin_access>
          <h2>You are an <b>admin</b></h2>
        </ProtectedContent>
        <ProtectedContent interpreter_access>
          <h2>You are an <b>interpreter</b></h2>
        </ProtectedContent>
        <ProtectedContent customer_access>
          <h2>You are a <b>customer</b></h2>
        </ProtectedContent>

        Choose an option from the navbar.
    </div>
    </>
    )
}

export default Landing;