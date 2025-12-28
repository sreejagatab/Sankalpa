import React, { ReactNode } from 'react';
import MainLayout from './MainLayout';

interface LayoutProps {
  children: ReactNode;
}

// Simple wrapper around MainLayout to maintain compatibility
const Layout: React.FC<LayoutProps> = ({ children }) => {
  return <MainLayout>{children}</MainLayout>;
};

export default Layout;