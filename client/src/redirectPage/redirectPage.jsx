import React, { useEffect, useState } from "react";
import TopAppBar from "../components/topAppBar";
import RedirectContent from "./redirectContent";
import { Button, Stack, Box } from "@mui/material";
import { useNavigate } from "react-router-dom";
// import _ from "lodash";
import { testAuthGetter } from "../utils/httpsFunction";
import { styled } from "@mui/material/styles";

const RedirectPage = (props) => {
  let navigate = useNavigate();
  const [isSuccess, setIsSuccess] = useState(false);
  const [successMessage, setSuccessMessage] = useState("");
  useEffect(() => {
    const cleanUpAuthToken = (str) => {
      return str.split("&")[1].slice(5);
    };
    async function authenticate() {
      try {
        const stravaAuthToken = cleanUpAuthToken(window.location.search);
        const response = await testAuthGetter(stravaAuthToken);
        if (response.success) {
          console.log("You have successfully registered your strava account.");
          setIsSuccess(true);
          setSuccessMessage(response.message);
        } else {
          throw new Error("Problem registering, please try again!");
        }
      } catch (error) {
        console.log(error);
      }
    }
    authenticate();
  }, []);

  const ColorButton = styled(Button)(() => ({
    color: "#ffffff",
    backgroundColor: "#000000",
    "&:focus": {
      backgroundColor: "#ffffff",
      color: "#000000",
    },
  }));

  const submitAccessToken = () => {
    console.log("Submitting token to backend");
    navigate("../home", { replace: true });
  };

  return (
    <>
      <TopAppBar />
      <Box
        component="form"
        height="auto"
        noValidate
        autoComplete="off"
        width="90%"
        margin="20px auto"
      >
        <Stack spacing={2}>
          <RedirectContent
            success={isSuccess}
            successMessage={successMessage}
            submitHandler={submitAccessToken}
          />
          <ColorButton
            variant="contained"
            onClick={() => submitAccessToken()}
            sx={{ backgroundColor: "#000000" }}
            disableRipple={true}
          >
            Click to go to Home page.
          </ColorButton>
        </Stack>
      </Box>
    </>
  );
};

export default RedirectPage;
