import { useEffect } from "react";
import { useLocation } from "wouter";

//https://github.com/molefrog/wouter/issues/316#issuecomment-1822264860 (can now send state if i need this!)
//https://github.com/molefrog/wouter/issues/290
// https://github.com/molefrog/wouter/pull/325

function ScrollToTop() {
  const  [ pathname ] = useLocation();

  useEffect(() => {
    window.scrollTo(0, 0);
  }, [pathname]);

  return null;
}

const useHistory = () => {
  const [location] = useLocation();

  const setLocation = (to, data) => {
    window.history.pushState(data, "", to);
  };

  return [location, setLocation, window.history.state];
};


export {ScrollToTop, useHistory}