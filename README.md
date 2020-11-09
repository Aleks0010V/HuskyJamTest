# HuskyJam test task

<pre>You can run an app with <code>docker-compose up</code> or <code>docker-compose up --build</code>
command for the first run. Ports 80 and 3306 must be free.</pre>

#### Endpoints
<p>Info about schemas etc. you can find on http://127.0.0.1/docs</p>
<table>
    <thead>
        <tr>
            <th>Method</th>
            <th>URL</th>
            <th>Description</th>
            <th>Access rights</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>POST</td>
            <td>/users/login</td>
            <td>an endpoint to receive JWT</td>
            <td>everyone</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/users/me</td>
            <td>an endpoint to fetch info about yourself</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>POST</td>
            <td>/users/create_user</td>
            <td>an endpoint to create new user</td>
            <td>everyone</td>
        </tr>
        <tr>
            <td>POST</td>
            <td>/users/update_user_info</td>
            <td>an endpoint to update your info</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/schedule</td>
            <td>fetch your schedule</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/schedule/list_masters</td>
            <td>fetch available masters</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/schedule/master/{master_id}</td>
            <td>fetch free hours of specific master</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>POST</td>
            <td>/schedule/create_an_appointment</td>
            <td>create a visit appointment for specific time to specific master</td>
            <td>authenticated users</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/admin/list_clients</td>
            <td>fetch all clients</td>
            <td>admin only</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/admin/client/{client_id}</td>
            <td>fetch appointments of specific client</td>
            <td>admin only</td>
        </tr>
        <tr>
            <td>GET</td>
            <td>/admin/master/{master_id}</td>
            <td>fetch specific masters schedule</td>
            <td>admin only</td>
        </tr>
        <tr>
            <td>POST</td>
            <td>/admin/create_master</td>
            <td>create new master profile</td>
            <td>admin only</td>
        </tr>
    </tbody>
</table>