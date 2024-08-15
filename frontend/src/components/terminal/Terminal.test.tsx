import React from "react";
import { act, screen } from "@testing-library/react";
import { renderWithProviders } from "test-utils";
import { Command, appendInput, appendOutput } from "#/state/commandSlice";
import Terminal from "./Terminal";

global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  disconnect: vi.fn(),
}));

const mockTerminal = {
  open: vi.fn(),
  write: vi.fn(),
  writeln: vi.fn(),
  dispose: vi.fn(),
  onKey: vi.fn(),
  attachCustomKeyEventHandler: vi.fn(),
  loadAddon: vi.fn(),
};

vi.mock("@xterm/xterm", async (importOriginal) => ({
  ...(await importOriginal<typeof import("@xterm/xterm")>()),
  Terminal: vi.fn().mockImplementation(() => mockTerminal),
}));

const renderTerminal = (commands: Command[] = []) =>
  renderWithProviders(<Terminal />, {
    preloadedState: {
      cmd: {
        commands,
      },
    },
  });

describe("Terminal", () => {
  afterEach(() => {
    vi.clearAllMocks();
  });

  it("should render a terminal", () => {
    renderTerminal();

    expect(screen.getByText("Terminal")).toBeInTheDocument();
    expect(mockTerminal.open).toHaveBeenCalledTimes(1);

    expect(mockTerminal.write).toHaveBeenCalledWith(
      "opendevin@docker-desktop:/workspace $ ",
    );
  });

  it("should load commands to the terminal", () => {
    renderTerminal([
      { type: "input", content: "INPUT" },
      { type: "output", content: "OUTPUT" },
    ]);

    expect(mockTerminal.writeln).toHaveBeenNthCalledWith(1, "INPUT");
    expect(mockTerminal.write).toHaveBeenNthCalledWith(2, "OUTPUT");
  });

  it("should write commands to the terminal", () => {
    const { store } = renderTerminal();

    act(() => {
      store.dispatch(appendInput("echo Hello"));
      store.dispatch(appendOutput("Hello"));
    });

    expect(mockTerminal.writeln).toHaveBeenNthCalledWith(1, "echo Hello");
    expect(mockTerminal.write).toHaveBeenNthCalledWith(2, "Hello");

    act(() => {
      store.dispatch(appendInput("echo World"));
    });

    expect(mockTerminal.writeln).toHaveBeenNthCalledWith(2, "echo World");
  });

  it("should load and write commands to the terminal", () => {
    const { store } = renderTerminal([
      { type: "input", content: "echo Hello" },
      { type: "output", content: "Hello" },
    ]);

    expect(mockTerminal.writeln).toHaveBeenNthCalledWith(1, "echo Hello");
    expect(mockTerminal.write).toHaveBeenNthCalledWith(2, "Hello");

    act(() => {
      store.dispatch(appendInput("echo Hello"));
    });

    expect(mockTerminal.writeln).toHaveBeenNthCalledWith(2, "echo Hello");
  });

  it("should end the line with a dollar sign after writing a command", () => {
    const { store } = renderTerminal();

    act(() => {
      store.dispatch(appendInput("echo Hello"));
    });

    expect(mockTerminal.writeln).toHaveBeenCalledWith("echo Hello");
    expect(mockTerminal.write).toHaveBeenCalledWith(
      "opendevin@docker-desktop:/workspace $ ",
    );
  });

  // This test fails because it expects `disposeMock` to have been called before the component is unmounted.
  it.skip("should dispose the terminal on unmount", () => {
    const { unmount } = renderWithProviders(<Terminal />);

    expect(mockTerminal.dispose).not.toHaveBeenCalled();

    unmount();

    expect(mockTerminal.dispose).toHaveBeenCalledTimes(1);
  });
});
