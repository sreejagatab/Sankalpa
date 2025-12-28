// Jest configuration for frontend tests
module.exports = {
  testEnvironment: 'jsdom',
  roots: ['<rootDir>/tests/frontend'],
  transform: {
    '^.+\\.(js|jsx|ts|tsx)$': ['babel-jest', { presets: ['next/babel'] }],
  },
  moduleNameMapper: {
    // Handle CSS imports
    '^.+\\.(css|less|scss)$': 'identity-obj-proxy',
    // Handle image imports
    '^.+\\.(jpg|jpeg|png|gif|webp|svg)$': '<rootDir>/tests/frontend/__mocks__/fileMock.js',
    // Handle module aliases
    '^@/components/(.*)$': '<rootDir>/frontend/components/$1',
    '^@/pages/(.*)$': '<rootDir>/frontend/pages/$1',
    '^@/hooks/(.*)$': '<rootDir>/frontend/hooks/$1',
    '^@/utils/(.*)$': '<rootDir>/frontend/utils/$1',
  },
  setupFilesAfterEnv: ['<rootDir>/tests/frontend/setupTests.js'],
  testPathIgnorePatterns: ['<rootDir>/node_modules/', '<rootDir>/.next/'],
  collectCoverage: true,
  collectCoverageFrom: [
    'frontend/**/*.{js,jsx,ts,tsx}',
    '!frontend/**/*.d.ts',
    '!frontend/**/_app.tsx',
    '!frontend/**/_document.tsx',
  ],
  coverageThreshold: {
    global: {
      branches: 70,
      functions: 70,
      lines: 70,
      statements: 70,
    },
  },
};
