import { useRef } from "react";
import {
  Box,
  Button,
  Text,
  Table,
  Thead,
  Td,
  Tr,
  Tbody,
  Flex,
  AlertDialog,
  AlertDialogBody,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogContent,
  AlertDialogOverlay,
  useDisclosure,
} from "@chakra-ui/react";

const VmInsight = ({ insight }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const cancelRef = useRef();
  return (
    <Box mb={2}>
      <Button
        onClick={onOpen}
        width="230px"
        colorScheme={insight.general?.toDelete ? "red" : "gray"}
      >
        {insight.tag}
      </Button>
      <AlertDialog
        isOpen={isOpen}
        leastDestructiveRef={cancelRef}
        onClose={onClose}
      >
        <AlertDialogOverlay>
          <AlertDialogContent maxW={"500px"}>
            <AlertDialogHeader fontSize="lg" fontWeight="bold">
              {insight.tag}
            </AlertDialogHeader>

            <AlertDialogBody>
              <Flex justifyContent="center" alignItems="center">
                {insight.general?.toDelete ? (
                  <Text>You can remove this virtual machine</Text>
                ) : (
                  <Table variant="simple">
                    <Thead>
                      <Tr background="teal">
                        <Td textAlign="center">Change</Td>
                        <Td textAlign="center">Current</Td>
                        <Td textAlign="center" background="teal">
                          Suggested
                        </Td>
                      </Tr>
                    </Thead>
                    <Tbody>
                      {insight.general.instance_size.prev !==
                        insight.general.instance_size.suggested && (
                        <Tr>
                          <Td textAlign="center" fontWeight="700">
                            Size
                          </Td>
                          <Td textAlign="center">
                            {insight.general.instance_size.prev}
                          </Td>
                          <Td textAlign="center" fontWeight="700">
                            {insight.general.instance_size.suggested}
                          </Td>
                        </Tr>
                      )}
                      {insight.general.max_resouce_volume.prev !==
                        insight.general.max_resouce_volume.suggested && (
                        <Tr>
                          <Td textAlign="center" fontWeight="700">
                            Resource Max Size
                          </Td>
                          <Td textAlign="center">
                            {insight.general.max_resouce_volume.prev}
                          </Td>
                          <Td textAlign="center" fontWeight="700">
                            {insight.general.max_resouce_volume.suggested}
                          </Td>
                        </Tr>
                      )}
                      <Tr>
                        <Td textAlign="center" fontWeight="700">
                          Price
                        </Td>

                        <Td textAlign="center">
                          {insight.pricing.current.price}
                          <br />
                          {insight.pricing.current.tag}
                        </Td>
                        <Td textAlign="center" fontWeight="700">
                          {insight.pricing.suggested.price}
                          <br />
                          {insight.pricing.suggested.tag}
                        </Td>
                      </Tr>
                    </Tbody>
                  </Table>
                )}
              </Flex>
            </AlertDialogBody>

            <AlertDialogFooter>
              <Button colorScheme="red" onClick={onClose} ml={3}>
                Close
              </Button>
            </AlertDialogFooter>
          </AlertDialogContent>
        </AlertDialogOverlay>
      </AlertDialog>
    </Box>
  );
};

export default VmInsight;
