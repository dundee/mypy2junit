import mypy2junit

def test_example():
    lines = open('tests/mypy.txt').readlines()
    res = mypy2junit.process_lines(lines)

    assert res == """<?xml version="1.0" encoding="utf-8"?>
<testsuite errors="0" failures="154" name="mypy" skips="0" tests="154" time="0.0">
    <testcase name="mylittlepony/mylittlepony/rpc/base.py:565" time="0.0">
        <failure message="No overload variant of &quot;get&quot; of &quot;Mapping&quot; matches argument types &quot;str&quot;, &quot;Dict[&lt;nothing>, &lt;nothing>]&quot;" type="WARNING">No overload variant of &quot;get&quot; of &quot;Mapping&quot; matches argument types &quot;str&quot;, &quot;Dict[&lt;nothing>, &lt;nothing>]&quot;</failure>
    </testcase>
    <testcase name="mylittlepony/mylittlepony/rpc/base.py:814" time="0.0">
        <failure message="Name 'xmlrpclib' is not defined" type="WARNING">Name 'xmlrpclib' is not defined</failure>
    </testcase>
    <testcase name="mylittlepony/mylittlepony/rpc/base.py:883" time="0.0">
        <failure message="Need type annotation for 'status_codes_to_exceptions' (hint: &quot;status_codes_to_exceptions: Dict[&lt;type>, &lt;type>] = ...&quot;)" type="WARNING">Need type annotation for 'status_codes_to_exceptions' (hint: &quot;status_codes_to_exceptions: Dict[&lt;type>, &lt;type>] = ...&quot;)</failure>
    </testcase>
    <testcase name="mylittlepony/mylittlepony/rpc/base.py:885" time="0.0">
        <failure message="Type signature has too few arguments" type="WARNING">Type signature has too few arguments</failure>
    </testcase>
</testsuite>"""
