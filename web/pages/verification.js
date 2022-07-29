import { useColorModeValue, Box, Heading, Button, Alert, AlertDescription, CloseButton, AlertIcon } from '@chakra-ui/react'
import { useEffect, useState } from 'react';
import styles from '../styles/Home.module.css'
import axios from "axios"
import { API_URL } from "../static";
import { useRouter } from 'next/router'
import OtpInput from 'react-otp-input';
import {useStore} from "./index"
import Router from 'next/router'
import { verification } from '@mokhta_s/react-statfive-api'


const Verification = () => {
    const [otp, setOtp] = useState("")
    const [error, setError] = useState(null)

    const bg = useColorModeValue("#0f0f1a", "blueteal.500")
    const token = useStore(state => state.token)
    const setCheck = useStore(state => state.setCheck)
    const data = useStore(state => state.data)
    const setData = useStore(state => state.addData)
    const addVerif = useStore(state => state.addVerif)
    const router = useRouter()

    const verif = async () => {
        if(otp.length < 1) {
            setError("Aucun champ n'a été rempli")
            return;
        }
        // let result = await verification(API_URL, otp, token, data.id);
        // console.log(result)
        // if(result && !(result?.data?.error)) {
        //     setData(result.data)
        //     addVerif(true)
        //     router.push('accueil')
        //     setCheck()
        // } else {
        //     console.log(result)
        //     setError(result.data.message)
        // }
    }

    useEffect(() => {
        if(data && data.verification === true) {
            Router.replace('/accueil')
        }
    }, [data])

    return (
        <Box bgColor={bg} className={styles.container}>
            <Heading color="white" mb="40px">Valider votre code reçu par mail :</Heading>
            {error && 
            <Alert status="error" borderRadius="10px" mb="10px">
            <AlertIcon />
            <AlertDescription mr={2}>{error}</AlertDescription>
            <CloseButton position="absolute" right="8px" top="8px" />
            </Alert>
            }
            <OtpInput
                color="#0f0f1a"
                value={otp}
                onChange={(otp) => setOtp(otp)}
                numInputs={4}
                separator={<span>|</span>}
                inputStyle={{
                    width: "50px",
                    height: "125px",
                    fontSize:"25px",
                    color:"#0f0f1a",
                    textTransform: "uppercase"
                }}
            />
            <Button colorScheme="teal" variant="outline" onClick={verif} mt="20px">Valider</Button>
        </Box>
    )
}

export default Verification