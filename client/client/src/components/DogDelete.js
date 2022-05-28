import { useState } from "react";
import { useLocation, useNavigate } from "react-router-dom";

const DogDelete = ({deleteHandler}) => {
    const location = useLocation();
    const dog = location.state.dog;
    const navigate = useNavigate();
    const [answer,setAnswer] = useState('No');
    const formHandler =(e)=>{
        e.preventDefault();
        
        if (answer=='Yes'){
            deleteHandler(dog);
            navigate('/dogs');
        }
        else
        {
            navigate('/dogs');
        }
    }
    return(
        <form onSubmit={formHandler}>
            <div>
                <label>ID: {dog.id}</label>
            </div>
            <div>
                <label>Name: {dog.name}</label>
            </div>
            <label>Are you sure you want to delete this dog? </label>
            <button onClick={(e)=>{setAnswer('Yes')}}>Yes</button>
            <button onClick={(e)=>{setAnswer('No')}}>No</button>
        </form>
    );
}
export default DogDelete;