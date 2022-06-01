%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/rolling/.*$
%global __requires_exclude_from ^/opt/ros/rolling/.*$

Name:           ros-rolling-moveit-kinematics
Version:        2.5.1
Release:        1%{?dist}%{?release_suffix}
Summary:        ROS moveit_kinematics package

License:        BSD
URL:            http://moveit.ros.org
Source0:        %{name}-%{version}.tar.gz

Requires:       eigen3-devel
Requires:       python%{python3_pkgversion}-lxml
Requires:       ros-rolling-class-loader
Requires:       ros-rolling-moveit-common
Requires:       ros-rolling-moveit-core
Requires:       ros-rolling-moveit-msgs
Requires:       ros-rolling-orocos-kdl-vendor
Requires:       ros-rolling-pluginlib
Requires:       ros-rolling-tf2
Requires:       ros-rolling-tf2-kdl
Requires:       ros-rolling-urdfdom
Requires:       ros-rolling-ros-workspace
BuildRequires:  eigen3-devel
BuildRequires:  ros-rolling-ament-cmake
BuildRequires:  ros-rolling-class-loader
BuildRequires:  ros-rolling-moveit-common
BuildRequires:  ros-rolling-moveit-core
BuildRequires:  ros-rolling-moveit-msgs
BuildRequires:  ros-rolling-orocos-kdl-vendor
BuildRequires:  ros-rolling-pluginlib
BuildRequires:  ros-rolling-tf2
BuildRequires:  ros-rolling-tf2-kdl
BuildRequires:  ros-rolling-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%if 0%{?with_tests}
BuildRequires:  ros-rolling-ament-cmake-gtest
BuildRequires:  ros-rolling-ament-lint-auto
BuildRequires:  ros-rolling-ament-lint-common
BuildRequires:  ros-rolling-launch-param-builder
BuildRequires:  ros-rolling-moveit-configs-utils
BuildRequires:  ros-rolling-moveit-resources-fanuc-description
BuildRequires:  ros-rolling-moveit-resources-fanuc-moveit-config
BuildRequires:  ros-rolling-moveit-resources-panda-description
BuildRequires:  ros-rolling-moveit-resources-panda-moveit-config
BuildRequires:  ros-rolling-moveit-ros-planning
BuildRequires:  ros-rolling-ros-testing
%endif

%description
Package for all inverse kinematics solvers in MoveIt

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/rolling" \
    -DAMENT_PREFIX_PATH="/opt/ros/rolling" \
    -DCMAKE_PREFIX_PATH="/opt/ros/rolling" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/rolling/setup.sh" ]; then . "/opt/ros/rolling/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/rolling

%changelog
* Wed Jun 01 2022 Henning Kayser <henningkayser@picknik.ai> - 2.5.1-1
- Autogenerated by Bloom

* Thu May 26 2022 Henning Kayser <henningkayser@picknik.ai> - 2.5.0-1
- Autogenerated by Bloom

