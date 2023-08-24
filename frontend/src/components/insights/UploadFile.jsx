import { useDropzone } from "react-dropzone";
import { Box, Button, Spinner, Text } from "@chakra-ui/react";

const DropBox = ({ onDrop, isMobile }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/json": [".json"],
    },
  });
  return (
    <Box
      {...getRootProps()}
      p={isMobile ? 0 : 4}
      border={isMobile ? "none" : "7px dashed"}
      borderColor="gray.200"
      borderRadius="20px"
      textAlign="center"
      mt={4}
      width={isMobile ? "auto" : "700px"}
      height={isMobile ? "auto" : "300px"}
      background="gray"
      display="flex"
      justifyContent="center"
      alignItems="center"
    >
      <input {...getInputProps()} />
      {isMobile ? (
        <Button
          colorScheme="teal"
          width="200px"
          height="70px"
          color={"white"}
          bg={"teal.400"}
        >
          Upload File
        </Button>
      ) : isDragActive ? (
        <Text fontSize={40} color="white">
          Drop the files here ...
        </Text>
      ) : (
        <Text fontSize={40} color="white">
          Drag 'n' drop your json file here, or click to select files
        </Text>
      )}
    </Box>
  );
};

const UploadFile = ({ fileName, onDrop, isMobile, message, isLoading }) => {
  return (
    <Box
      display="flex"
      flexDirection="column"
      justifyContent="flex-start"
      alignItems="center"
      mt="20px"
    >
      {!fileName && <DropBox onDrop={onDrop} isMobile={isMobile} />}
      {fileName && !message ? (
        <Text fontSize="20px">{"file name: " + fileName}</Text>
      ) : (
        ""
      )}
      {message && <Text>{message}</Text>}
      {isLoading && fileName && (
        <>
          <Spinner size="xl" mt="100px" color="teal.400"></Spinner>
          <Text mt={5} color="teal.400">
            Getting your insights...
          </Text>
        </>
      )}
    </Box>
  );
};

export default UploadFile;
