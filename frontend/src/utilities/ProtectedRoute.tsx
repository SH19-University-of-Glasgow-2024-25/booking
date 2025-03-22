import React, { useContext, useEffect, useState } from 'react';
import { Navigate } from 'react-router-dom';
import apiClient from './apiClient';
import AccountContext from './authenticationContext';

interface ProtectedRouteProps {
    children: React.ReactNode;
    admin_access?: boolean;
    interpreter_access?: boolean;
    customer_access?: boolean;
}

const ProtectedRoute: React.FC<ProtectedRouteProps> = (
    {
        children,
        admin_access = false,
        interpreter_access = false,
        customer_access = false,
    }
) => {
    const { accountType, setAccountType } = useContext(AccountContext);
    const [isAuthenticated, setIsAuthenticated] = useState<boolean | null>(null);

    useEffect(() => {
        // Send a request to check if the user is authenticated
        const checkAuth = async () => {
            try {
                await apiClient.get('/check-auth/')
                .then((res) => {
                    setAccountType(res.data.result.account_type);
                    setIsAuthenticated(true);
                })
            } catch {
                setIsAuthenticated(false);
            }
        };

        if (accountType) {
            setIsAuthenticated(true);
        } else {
            checkAuth();
        }
    }, []);

    // While checking authentication show nothing
    if (isAuthenticated === null) {
        return null;
    }

    if (
        isAuthenticated &&
        (
            (accountType == "A" && admin_access) ||
            (accountType == "C" && customer_access) ||
            (accountType == "I" && interpreter_access)
        )
    ) {
        return <>{children}</>;
    }

    return <Navigate to="/login" />;
};

export default ProtectedRoute;
