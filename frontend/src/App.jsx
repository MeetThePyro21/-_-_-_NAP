import React, { useState, useEffect } from "react";
import "./App.css"

export default function App() {

    const upload_url = "http://127.0.0.1:8000/upload_files"
    const get_img_url = "http://127.0.0.1:8000/get_out"
    const get_map = "http://127.0.0.1:8000/get_map"
    
    const [uploadStatus, setUploadStatus] = useState(".")
    const [img, setImg] = useState();
    const [type, setType] = useState("upload");
 
    useEffect(() => {
        fetch(get_img_url)
            .then(res => res.json())
        fetchImage();
    }, [uploadStatus])

    const onImageChange = (event) => {
        if (event.target.files && event.target.files[0]) {
            sendImg(event.target.files)
        }
    }

    const sendImg = (files) => {
        let formData = new FormData()
        
        for (let i = 0; i < files.length; i++) {
            formData.append('files', files[i], files[i].name)
        }

        const values = [...formData.entries()];
        console.log(values);
        fetch(upload_url, {
            method: "POST",
            body: formData

        })
            .then(setUploadStatus(".."))
    }

    const fetchImage = async () => {
        const res = await fetch(get_img_url);
        const imageBlob = await res.blob();
        const imageObjectURL = URL.createObjectURL(imageBlob);
        setImg(imageObjectURL);
        setUploadStatus("...")
    };

    let content;

    switch (type) {
        default:
        case "upload":
            content = (
                <div>

            <div className="body"></div>

                    <div className="title">
                        Прогнозирование покупок клиентами ПАО «Ростелеком»
                    </div>
                     
                    <div className="upload">
                        <input type="file" class="inputfile" onChange={onImageChange} multiple/>
                    </div>
                    
                    <div className="show_result">
                        <button onClick={() => { setType("show_image") }}> Результат </button>
                    </div>


                    <div className="iframe">
                            <iframe  width='1000' height='500' src={get_map} alt="not iframe" />
                    </div>


                </div>
            )
            break
        case "show_image":
                content = (
                    <div>
                       <div className="back">
                            <img src={get_img_url} alt="not image" />
                        </div>
                        
                        <div className="back">
                            <button onClick={() => { setType("upload") }}>назад</button>
                        </div>
                    </div>
                )
                break
        }

    return content
}