<html>
    <title>Gitlab webhook runner configurator</title>
<body>
    <p>
        Errors occurred during SSH configuration:
        <ul>
        % for e in errors:
            <li>${e}</li>
        % endfor
        </ul>
    </p>
    <a href="javascript:history.go(-1)">Back</a>
</body>
</html>
