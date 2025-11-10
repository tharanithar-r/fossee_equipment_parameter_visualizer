import { LogOut, Moon, Sun } from "lucide-react";
import { Button } from "./ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { useTheme } from "@/contexts/ThemeContext";

const NavBar = () => {

    const { logout } = useAuth();
    const { theme, toggleTheme } = useTheme();

    return (
        <header className="fixed top-0 left-0 right-0 z-50 px-4 pt-4">
            <div className="max-w-7xl mx-auto">
            <div className="relative backdrop-blur-xl bg-gradient-to-r rounded-2xl border border-border shadow-xl">
                <div className="px-6 py-4 flex justify-between items-center">
                <h1 className="text-2xl font-bold text-foreground">
                    Chemical Equipment Visualizer
                </h1>
                <div className="flex items-center gap-2">
                    <Button
                    variant="outline"
                    size="icon"
                    onClick={toggleTheme}
                    className="hover:bg-primary/10 transition-colors"
                    >
                    {theme === 'light' ? <Moon className="h-5 w-5" /> : <Sun className="h-5 w-5" />}
                    </Button>
                    <Button
                    variant="secondary"
                    onClick={logout}
                    className="hover:bg-destructive/10 hover:text-destructive transition-colors"
                    >
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                    </Button>
                </div>
                </div>
            </div>
            </div>
        </header>
    )
}

export {NavBar};