import Sidebar from '../components/Sidebar';

export default function Layout({ children }) {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 flex flex-col">
        <div className="gradient-bar" />
        {children}
      </main>
    </div>
  );
}
