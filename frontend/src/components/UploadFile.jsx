import React, { useState } from "react";
import { useDropzone } from "react-dropzone";
import { Box, Button, Flex, Text, useBreakpointValue } from "@chakra-ui/react";
import { Input } from "@chakra-ui/react";

const DropBox = ({ onDrop, setFileName }) => {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });
  return (
    <>
      <Box
        {...getRootProps()}
        p={4}
        border="7px dashed"
        borderColor="gray.200"
        borderRadius="20px"
        textAlign="center"
        mt={4}
        width="70%"
        height="300px"
        opacity="0.4"
        background="gray"
        display="flex"
        justifyContent="center"
        alignItems="center"
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <Text>Drop the files here ...</Text>
        ) : (
          <Text fontSize={40} color="white">
            Drag 'n' drop some files here, or click to select files
          </Text>
        )}
      </Box>
    </>
  );
};

const UploadFile = React.forwardRef((props, ref) => {
  const [fileName, setFileName] = useState(null);
  const isMobile = useBreakpointValue({ base: true, lg: false });
  const onDrop = React.useCallback((acceptedFiles) => {
    setFileName(acceptedFiles[0].path);
    console.log(acceptedFiles);
  }, []);
  return (
    <Flex
      ref={ref}
      direction="column"
      justifyContent="flex-start"
      alignItems="center"
      height="600px"
      m={0}
    >
      {!fileName && !isMobile && (
        <DropBox setFileName={setFileName} onDrop={onDrop} />
      )}
      {!fileName && isMobile && (
        <Box
          as="label"
          width="150px"
          height="50px"
          position="relative"
          display="inline-block"
          px={4}
          py={2}
          cursor="pointer"
          fontSize="23px"
          fontWeight="500"
          color="white"
          borderRadius="md"
          bg="teal.500"
          _hover={{
            bg: "teal.400",
          }}
          textAlign="center"
        >
          Upload File
          <Input
            type="file"
            opacity="0"
            position="absolute"
            width="100%"
            height="100%"
            left="0"
            top="0"
            cursor="pointer"
          />
        </Box>
      )}
      {fileName ? <Text fontSize="25px">{fileName}</Text> : ""}
    </Flex>
  );
});

export default UploadFile;
