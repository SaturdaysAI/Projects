import "./globals.css";

export const metadata = {
  title: "SmartBite: Eat wiser",
  description: "SmartBite is an AI tool to detect food and display nutritional information",
};

export default function RootLayout({ children }) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
