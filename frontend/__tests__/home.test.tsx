import { render, screen } from "@testing-library/react";
import Home from "../app/page";
import { describe, it, expect, vi } from "vitest";

vi.mock("next/link", () => ({
  default: ({ href, children }: { href: string; children: React.ReactNode }) => (
    <a href={href}>{children}</a>
  ),
}));

describe("Home page", () => {
  it("renders the hero headline", () => {
    render(<Home />);
    expect(
      screen.getByRole("heading", {
        name: /Executable AI Policies for Higher Education/i,
      })
    ).toBeInTheDocument();
  });

  it("renders primary navigation links", () => {
    render(<Home />);
    expect(screen.getByRole("link", { name: /Faculty Builder/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Student Copilot/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Student Dashboard/i })).toBeInTheDocument();
    expect(screen.getByRole("link", { name: /Admin Analytics/i })).toBeInTheDocument();
  });

  it("renders policy status section", () => {
    render(<Home />);
    expect(screen.getByText(/Policy Status/i)).toBeInTheDocument();
    expect(screen.getByText(/CS101 AI Policy/i)).toBeInTheDocument();
  });
});
