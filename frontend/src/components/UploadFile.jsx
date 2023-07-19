import React from "react";
import { useDropzone } from "react-dropzone";
import { Box, Flex, Text } from "@chakra-ui/react";

const UploadFile = React.forwardRef((props, ref) => {
  const onDrop = React.useCallback((acceptedFiles) => {
    // Do something with the files
    console.log(acceptedFiles);
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({ onDrop });

  return (
    <Flex
      ref={ref}
      direction="column"
      justifyContent="center"
      alignItems="center"
    >
      <Box
        {...getRootProps()}
        p={4}
        border="2px dashed"
        borderColor="gray.200"
        borderRadius="20px"
        textAlign="center"
        mt={4}
        width="70%"
      >
        <input {...getInputProps()} />
        {isDragActive ? (
          <Text>Drop the files here ...</Text>
        ) : (
          <Text>Drag 'n' drop some files here, or click to select files</Text>
        )}
      </Box>
    </Flex>
  );
});

export default UploadFile;
