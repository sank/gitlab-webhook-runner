<html>
    <title>Gitlab webhook runner configurator</title>
<body>
    <form action="/gitlab/docker_config" method="POST">
        <p>
            This docker service connects to your server via ssh and runs the script on that server.
            <br/>
            Enter host, user and password for access to script on your server by ssh.
        </p>

        <table>
            <tr>
                <th>
                    <label>Hostname:</label>
                </th>
                <td>
                    ${hostname}
                </td>
            </tr>
            <tr>
                <th>
                    <label>Username:</label>
                </th>
                <td>
                    ${username}
                </td>
            </tr>
            <tr>
                <th>
                    <label>Enter password:</label>
                </th>
                <td>
                    <input type="password" name="password" value="">
                </td>
            </tr>
            <tr>
                <th>

                </th>
                <td>
                    <input type="submit" name="submit" value="Submit">
                </td>
            </tr>
        </table>
    </form>
</body>
</html>