import React, { useContext, useEffect} from "react";
import { Context } from "../store/appContext";
import { useNavigate } from "react-router-dom";

export const Private = () => {
    const{store,actions} = useContext(Context)
    const navigate = useNavigate()

    useEffect(() => {
        if (store.token && store.token !== '' && store.token !== undefined ?
        navigate('/private')
        :
        navigate('/login'))
        ;
    },[store.token])
    return(
        <div>Private Page</div>
    )
}