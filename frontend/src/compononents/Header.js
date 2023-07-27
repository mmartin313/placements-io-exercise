export function Header({ sideMenuOpen, setSideMenuOpen }) {
  return (
    <div className="relative flex h-16 flex-auto bg-white px-4 shadow drop-shadow-sm">
      <div
        onClick={() => {
          setSideMenuOpen((prevValue) => {
            return !prevValue;
          });
        }}
        className="flex place-items-center gap-8 place-self-center"
      >
        <a href="/">
          <span className="text-2xl font-black text-black">Campaigns</span>
        </a>
      </div>
    </div>
  );
}
