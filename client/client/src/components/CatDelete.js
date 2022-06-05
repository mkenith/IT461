import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const CatDelete = ({deleteHandler}) => {
    const location = useLocation();
    const cat = location.state.cat;
    const navigate = useNavigate();
    const [answer,setAnswer] = useState('No');
    const formHandler =(e)=>{
        e.preventDefault();
        
        if (answer=='Yes'){
            deleteHandler(cat);
            navigate('/cats');
        }
        else
        {
            navigate('/cats');
        }
    }
    return(
        <form onSubmit={formHandler}>
            <div>
                <label>ID: {cat.id}</label>
            </div>
            <div>
                <label>Name: {cat.name}</label>
            </div>
            <label>Are you sure you want to delete this cat? </label>
            <button onClick={(e)=>{setAnswer('Yes')}}>Yes</button>
            <button onClick={(e)=>{setAnswer('No')}}>No</button>
        </form>
    );
}
export default CatDelete;