import './App.css';

import { Routes,Route,Link,NavLink } from 'react-router-dom';
import HomePage from './pages/HomePage'
// import { useLocation } from "react-router-dom";
import { Container } from 'semantic-ui-react';
import ViewMarkdown from './pages/ViewMarkdown';
import EditMarkDown from './pages/EditMarkDown';


function App() {
  // const [setuser, setUser] = useState(null)
  // const location = useLocation();
  // console.log(location, " useLocation Hook");
  // useEffect(()=>{
  //   const user = location.state?.user;
  //   setUser(user)

  // },[location.state?.user])
  

  return (
    <div className="App">
      
      <header className="App-header">
        <p className="App-title">
          <NavLink to="/">Free World</NavLink>
        </p>
        {/* <div>
          {setuser?"":<div><Link to="/signin">Login</Link></div>}
          {setuser?"":<div><Link to="/signup">SignUp</Link></div>}
          <div><Link to="/api" state={{setuser:setuser}}>API</Link></div>
        </div> */}
        <div>
          {/* {<div><Link to="/">Home</Link></div>} */}
          {<div><Link to="/bot/home">View</Link></div>}
          {<div><Link to="/bot/home/edit">Edit</Link></div>}
        </div>
      </header>
      <Container>
      <div className="main">
        <Routes>
          <Route path="/" element={<HomePage/>}/>
          <Route path="/bot/home" element={<ViewMarkdown/>}/>
          <Route path="/bot/home/edit" element={<EditMarkDown/>}/>
        </Routes>
      </div>
      </Container>
    </div>
  );
}

export default App;
