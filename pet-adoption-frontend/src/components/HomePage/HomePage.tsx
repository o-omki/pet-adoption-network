import MainContent from "./Maincontent";
import Leftpanel from "./LeftPanel";
import Rightpanel from "./RightPanel";
import Searchbar from "./Searchbar";

export default function Homepage() {
  return (
    <div className="relative min-h-[200vh] overflow-y-auto p-10 pb-10 sm:p-10 mt-0 font-[family-name:var(--font-geist-sans)]">
      
      {/* Fixed Search Panel */}
      <div >
        <Searchbar />
      </div>

      {/* Main Page Layout (Scrolls Below) */}
      <div className="grid grid-cols-[15%_70%_15%] gap-4 mt-20">
        
        {/* Left Sidebar */}
        <div>
          <Leftpanel />
        </div>

        {/* Main Content */}
        <MainContent />

        {/* Right Sidebar */}
        <div>
          <Rightpanel />
        </div>
      </div>
    </div>
  );
}
