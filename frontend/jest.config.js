
export default {
    testEnvironment: "jest-environment-jsdom",
    transform: {
      "^.+\\.(t|j)sx?$": "babel-jest", // Use Babel for TS
    },
    roots: ["<rootDir>/src/__tests__"],
    setupFilesAfterEnv: ["<rootDir>/src/setupTests.js"],
    moduleNameMapper: {
      "\\.(css|scss|sass)$": "identity-obj-proxy"
    }
  };