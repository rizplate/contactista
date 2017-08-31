/* eslint-env browser */
import {
  commitMutation,
  graphql,
} from 'react-relay';

const mutation = graphql`
  mutation LoginMutation(
    $input: LoginInput!
  ) {
    login(input:$input) {
      token
      viewer {
        id
        username
      }
    }
  }
`;

let tempID = 0;

function commit(
  environment,
  username,
  password
) {
  return commitMutation(
    environment,
    {
      mutation,
      variables: {
        input: {
          username,
          password,
          clientMutationId: tempID++,
        },
      },
      onCompleted: (response) => {
        sessionStorage.setItem('token', response.login.token)
        // need a way to reload the environment...
      }
    }
  );
}

export default {commit};
