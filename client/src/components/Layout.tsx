/**
 * 페이지 레이아웃 컴포넌트
 */

import type { ReactNode } from "react";
import Navbar from "./Navbar";
import "./Layout.css";

interface LayoutProps {
    children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
    return (
        <div className="layout">
            <Navbar />
            <main className="main-content">{children}</main>
            <div className="container">
                <p className="footer-text">© 2025 동아리 플랫폼. All rights reserved.</p>
            </div>
        </div>
    );
};

export default Layout;
