<h1 id="django-riak-sessions">Django Riak Sessions</h1>
<div class="figure">
<img src="https://secure.travis-ci.org/flashingpumpkin/django-riak-sessions.png" /><p class="caption"></p>
</div>
<h2 id="installation">Installation</h2>
<p>Due to the <a href="http://code.google.com/p/protobuf/">protobuf</a> having had a <a href="http://code.google.com/p/protobuf/issues/detail?id=66">long standing issue</a> of not installing from PyPI the installation involves two steps:</p>
<pre><code>pip install protobuf -U
pip install django-riak-sessions</code></pre>
<h2 id="configuration">Configuration</h2>
<ul>
<li>Add <code>riak_sessions</code> to your installed apps</li>
<li><p>Add the session engine to your settings:</p>
<p>SESSION_ENGINE = 'riak_sessions.backends.riak'</p></li>
</ul>
<h2 id="optional-configuration">Optional Configuration</h2>
<p>There are a couple of optional configuration values. The default values are as follows:</p>
<pre class="sourceCode python"><code class="sourceCode python"><span class="ch">import</span> riak
RIAK_PORT = <span class="dv">8087</span>
RIAK_HOST = <span class="st">&#39;127.0.0.1&#39;</span>
RIAK_TRANSPORT_CLASS = riak.RiakPbcTransport
RIAK_BUCKET = <span class="st">&#39;django-riak-sessions&#39;</span>
RIAK_SESSION_KEY = <span class="st">&#39;session:</span><span class="ot">%(session_key)s</span><span class="st">&#39;</span></code></pre>
<p>To use secondary indexes, enable <a href="http://wiki.basho.com/LevelDB.html">LevelDB</a>:</p>
<pre class="sourceCode python"><code class="sourceCode python">RIAK_SESSION_USE_2I = <span class="ot">False</span></code></pre>
