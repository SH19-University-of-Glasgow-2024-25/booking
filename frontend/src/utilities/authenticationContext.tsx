import { createContext } from 'react';

interface AuthContextType {
    accountType: string | null;
    setAccountType: (type: string | null) => void;
  }

const AccountContext = createContext<AuthContextType>({
    accountType: null,
    setAccountType: () => {}
});

export default AccountContext;